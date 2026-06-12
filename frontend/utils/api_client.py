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

    try:

        response = requests.post(
            f"{BASE_URL}/upload",
            files=files,
            timeout=120
        )

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        return {
            "status_code": response.status_code,
            "body": response.text
        }

    except Exception as e:

        return {
            "status_code": -1,
            "body": str(e)
        }