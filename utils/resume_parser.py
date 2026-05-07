from pathlib import Path

import pdfplumber
import docx2txt


def extract_resume_text(file_path):
    """
    Extract text from PDF, DOCX, or TXT resume files.
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        return ""


def extract_text_from_pdf(file_path):
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        text = f"Error reading PDF file: {e}"

    return text.strip()


def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(str(file_path))
        return text.strip()

    except Exception as e:
        return f"Error reading DOCX file: {e}"


def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read().strip()

    except Exception as e:
        return f"Error reading TXT file: {e}"