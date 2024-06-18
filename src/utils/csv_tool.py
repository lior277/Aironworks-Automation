import csv
from typing import List


class CSVTool:
    @classmethod
    def create_file(cls, data, fieldnames: List[str], file_path: str, data_to_update: dict = None):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            data_to_write = {}
            if not isinstance(data, dict):
                if isinstance(data, list):
                    if getattr(data[0], "to_csv_file", None) and callable(data[0].to_csv_file):
                        data_to_write = [row.to_csv_file() for row in data]
                    else:
                        data_to_write = [row.get_body() for row in data]
                else:
                    data_to_write = data.get_body()
            if data_to_update:
                for item in data_to_write:
                    item.update(data_to_update)
            writer.writeheader()
            writer.writerows(data_to_write)
