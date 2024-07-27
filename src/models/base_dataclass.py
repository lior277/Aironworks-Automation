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
            field_types = get_type_hints(cls)
            return cls(
                **{
                    f: from_dict(field_types[f], data[f])
                    for f in data
                    if f in field_types
                }
            )
        elif isinstance(data, list):
            elem_type = cls.__args__[0]
            return [from_dict(elem_type, item) for item in data]
        else:
            return data

    def to_filtered_dict(self):
        return {
            key: self._convert_value(value)
            for key, value in self.__dict__.items()
            if value is not None
        }

    def _convert_value(self, value):
        if hasattr(value, 'to_filtered_dict'):
            return value.to_filtered_dict()
        elif isinstance(value, list):
            return [self._convert_value(item) for item in value]
        elif isinstance(value, dict):
            return {k: self._convert_value(v) for k, v in value.items()}
        else:
            return value


def from_dict(data_class: Type[T], data: Any) -> T:
    if isinstance(data, dict):
        field_types = get_type_hints(data_class)
        return data_class(
            **{f: from_dict(field_types[f], data[f]) for f in data if f in field_types}
        )
    elif isinstance(data, list):
        elem_type = data_class.__args__[0]
        return [from_dict(elem_type, item) for item in data]
    else:
        return data
