import json
from typing import List


class JSONTool:
    @classmethod
    def create_file(cls, data, file_path: str, data_to_update: dict = None) -> str:
        data_to_write = _validate_data(data)

        # Update each item if data_to_update is provided
        if data_to_update:
            for item in data_to_write:
                item.update(data_to_update)

        # Write the data to a JSON file
        with open(file_path, mode='w') as file:
            json.dump(data_to_write, file, indent=4)

        return file_path

    @classmethod
    def update_json_file(cls, file_path: str, data_to_update) -> str:
        # Load existing JSON data
        with open(file_path, mode='r') as file:
            existing_data = json.load(file)

        # Update the existing data with the new data
        validated_data_to_update = _validate_data(data_to_update)
        for i, item in enumerate(validated_data_to_update):
            if i < len(existing_data):
                existing_data[i].update(item)
            else:
                existing_data.append(item)

        # Save the updated data back to the JSON file
        with open(file_path, mode='w') as file:
            json.dump(existing_data, file, indent=4)

        return file_path

    @classmethod
    def create_json_file(cls, data, fieldnames: List[str], file_path: str) -> str:
        data_to_write = _validate_data(data)
        with open(file_path, mode='w') as file:
            json.dump(data_to_write, file, indent=4)
        return file_path


def _validate_data(data) -> list[dict]:
    if isinstance(data, dict):
        return [data]
    elif isinstance(data, list):
        return [
            row.to_json_file()
            if callable(getattr(row, 'to_json_file', None))
            else row.get_body()
            for row in data
        ]
    return (
        [data.to_json_file()]
        if callable(getattr(data, 'to_json_file', None))
        else [data.get_body()]
    )
