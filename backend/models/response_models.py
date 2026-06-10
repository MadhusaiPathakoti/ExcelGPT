from pydantic import BaseModel


class UploadResponse(BaseModel):

    file_name: str

    rows: int

    columns: int

    column_names: list

    data_types: dict

    preview: list