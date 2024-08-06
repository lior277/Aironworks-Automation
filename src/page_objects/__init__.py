from pathlib import Path

from src.utils.file_tool import convert_bytes

created_new_scenario_text = 'Created new scenario'
update_succeeded_text = 'Update succeeded'
failed_upload_file_text = 'Failed to upload file'
unrecognized_file_format_text = 'Unrecognized file format'
file_type_must_be_csv_xlsx = '- File type must be .csv, .xlsx'


def get_file_size_error_message(file_path: str):
    return f'- {convert_bytes(Path(file_path).stat().st_size)}'
