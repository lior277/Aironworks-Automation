import csv


class CSVTool:
    @staticmethod
    def write_rows(file_path: str, rows: list[dict]) -> str:
        if not rows:
            return file_path

        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        return file_path
