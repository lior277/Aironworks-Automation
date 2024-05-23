import csv
from typing import List


class CSVTool:
    @classmethod
    def create_file(cls, data, fieldnames: List[str], file_path: str):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            data_to_write = {}
            if not isinstance(data, dict):
                if isinstance(data, list):
                    data_to_write = [row.get_body() for row in data]
                else:
                    data_to_write = data.get_body()
            writer.writeheader()
            writer.writerows(data_to_write)
