import json
from dataclasses import fields

from typing import Type, TypeVar, Any, get_type_hints, List

T = TypeVar('T')


class BaseDataClass:
    def without_nullable(self):
        dict_result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                dict_result[key] = value
        return dict_result

    def get_body(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.__dict__)

    def get_fieldnames(self) -> List[str]:
        return [field.name for field in fields(self.__class__)]

    @classmethod
    def from_dict(cls: Type[T], data: Any) -> T:
        if isinstance(data, dict):
            fieldtypes = get_type_hints(cls)
            return cls(**{f: from_dict(fieldtypes[f], data[f]) for f in data if f in fieldtypes})
        elif isinstance(data, list):
            elem_type = cls.__args__[0]  # Assuming homogeneous lists
            return [from_dict(elem_type, item) for item in data]
        else:
            return data


def from_dict(data_class: Type[T], data: Any) -> T:
    if isinstance(data, dict):
        fieldtypes = get_type_hints(data_class)
        return data_class(**{f: from_dict(fieldtypes[f], data[f]) for f in data if f in fieldtypes})
    elif isinstance(data, list):
        elem_type = data_class.__args__[0]  # Assuming homogeneous lists
        return [from_dict(elem_type, item) for item in data]
    else:
        return data
