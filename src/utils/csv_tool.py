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


def _validate_data(data) -> dict:
    data_to_write = {}
    if not isinstance(data, dict):
        if isinstance(data, list):
            if getattr(data[0], 'to_csv_file', None) and callable(data[0].to_csv_file):
                data_to_write = [row.to_csv_file() for row in data]
            else:
                data_to_write = [row.get_body() for row in data]
        else:
            data_to_write = data.get_body()
    return data_to_write
