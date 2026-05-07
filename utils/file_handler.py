from pathlib import Path
from config.settings import UPLOAD_FOLDER


def save_uploaded_file(uploaded_file):
    Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    file_path = Path(UPLOAD_FOLDER) / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(file_path)