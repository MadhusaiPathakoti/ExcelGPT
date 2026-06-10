from pathlib import Path
import pandas as pd


class ExcelLoader:

    @staticmethod
    def load_excel(file_path: str):
        return pd.read_excel(file_path)

    @staticmethod
    def get_metadata(df):

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "data_types": {
                col: str(dtype)
                for col, dtype in df.dtypes.items()
            }
        }