import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:latest"


def generate_response(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "30m",
        "options": {
            "temperature": 0.1,
            "num_predict": 120,
            "num_ctx": 1024,
            "top_p": 0.8
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=240
        )
        response.raise_for_status()
        return response.json().get("response", "")

    except requests.exceptions.ReadTimeout:
        return (
            "Ollama timeout: interview questions took too long. "
            "Try again or use shorter resume/job text."
        )

    except requests.exceptions.ConnectionError:
        return "Ollama connection error: make sure Ollama is running."

    except Exception as e:
        return f"Ollama error: {e}"