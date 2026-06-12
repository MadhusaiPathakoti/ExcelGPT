import requests

BASE_URL = "https://excelgpt-2zrp.onrender.com/api"


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
        files=files,
        timeout=120
    )

    print(
        "UPLOAD STATUS:",
        response.status_code
    )

    print(
        "UPLOAD RESPONSE:",
        response.text[:500]
    )

    response.raise_for_status()

    return response.json()