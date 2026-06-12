import requests

BASE_URL = "https://excelgpt-2zrp.onrender.com"


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

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code != 200:
        raise Exception(
            f"Backend Error {response.status_code}: {response.text}"
        )

    return response.json()