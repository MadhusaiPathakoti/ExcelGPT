import requests

BASE_URL = "http://localhost:8000/api"


def upload_file(file):

    files = {
        "file": (
            file.name,
            file,
            file.type
        )
    }

    response = requests.post(
        f"{BASE_URL}/upload",
        files=files
    )

    response.raise_for_status()

    return response.json()