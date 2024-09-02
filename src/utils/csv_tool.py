import csv
from typing import List

import pandas as pd
from pandas import DataFrame


class CSVTool:
    @classmethod
    def create_file(
        cls, data, fieldnames: List[str], file_path: str, data_to_update: dict = None
    ) -> str:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            data_to_write = _validate_data(data)
            if data_to_update:
                for item in data_to_write:
                    item.update(data_to_update)
            writer.writeheader()
            writer.writerows(data_to_write)
        return file_path

    @classmethod
    def update_csv_file(cls, file_path: str, data_to_update) -> str:
        df = pd.read_csv(file_path)
        df.update(_validate_data(data_to_update))
        df.to_csv(file_path, index=False)
        return file_path

    @classmethod
    def create_xlsx_file(cls, data, fieldnames: List[str], file_path: str) -> str:
        df = DataFrame(_validate_data(data), columns=fieldnames)
        df.to_excel(file_path, index=False)
        return file_path


def _validate_data(data) -> dict | list[dict]:
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        return [
            row.to_csv_file()
            if callable(getattr(row, 'to_csv_file', None))
            else row.get_body()
            for row in data
        ]

    return (
        [data.to_csv_file()]
        if callable(getattr(data, 'to_csv_file', None))
        else [data.get_body()]
    )
