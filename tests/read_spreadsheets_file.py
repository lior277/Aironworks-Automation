import pandas as pd
import pygsheets

from src.configs.config_loader import AppFolders


def generate_testrail_csv(file_key: str):
    gc = pygsheets.authorize(
        client_secret=f'{AppFolders.RESOURCES_PATH}/client_secret.json',
        service_account_file=f'{AppFolders.RESOURCES_PATH}/secret-key.json',
    )
    columns = [
        'Title',
        'Section',
        'References',
        'Preconditions',
        'Steps',
        'Expected Result',
        'Priority',
    ]
    spreadsheet_file = gc.open_by_key(file_key)
    worksheets = spreadsheet_file.worksheets()
    all_data = []
    title = spreadsheet_file.title

    for worksheet in worksheets:
        if not worksheet.hidden:
            values = worksheet.get_as_df().values
            if 'TC ID' in values:
                section = values[1][3]
                link = values[2][3]
                index = 0
                for row in values:
                    if row[7] != '' and 'Precondition' != row[7]:
                        if row[3]:
                            category = row[3]
                        if row[4]:
                            sub_category1 = row[4]
                        if row[5]:
                            sub_category2 = row[5]
                        if row[6]:
                            sub_category3 = row[6]
                        data = [
                            f'[{category} {sub_category1} {sub_category2}] - {sub_category3}',
                            section,
                            link,
                            f'{row[7]}',
                            f'{row[8]}',
                            f'{row[9]}',
                            f'{row[10] if row[10] else "Medium"}',
                        ]
                        all_data.insert(index, data)
                        index += 1
        file_name = f'{AppFolders.RESOURCES_PATH}{title}.csv'
        pd.DataFrame(data=all_data, columns=columns).to_csv(file_name)
    return file_name


if __name__ == '__main__':
    # files = ["1w7X6O_fCM0Z1IwBt6ezT3Hqwc0mz6XTU2kjXNZTT_zU"]
    # be sure that file shared access with service-account@aironworkstest.iam.gserviceaccount.com
    files = ['1KoHGgsuCMl3rgqicqgkUfbYrCz_VYboW5I0znjUYl4k']
    for file in files:
        file = generate_testrail_csv(file)
        print(f'CSV files was created to import in TestRail: {file}')
