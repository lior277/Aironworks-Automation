from typing import Any


def divide_list_into_chunks(input_list: [Any], chunk_size: int):
    return [list(input_list[x:y]) for (x, y) in [(x, x + chunk_size) for x in range(0, len(input_list), chunk_size)]]
