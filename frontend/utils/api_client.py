import requests

BASE_URL = "https://excelgpt-2zrp.onrender.com/api"


def upload_file(uploaded_files):

    files_payload = []

    for file in uploaded_files:

        files_payload.append(

            (
                "files",
                (
                    file.name,
                    file,
                    file.type
                )
            )
        )

    response = requests.post(
        f"{BASE_URL}/upload",
        files=files_payload,
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

    if response.status_code != 200:

        return {
            "error": True,
            "status_code": response.status_code,
            "body": response.text
        }
    return response.json()