from dataclasses import fields

from src.models.company.localized_configs_model import Data
from src.models.company.patch_localized_configs_model import PatchLocalizedConfigsModel


class PatchLocalizedConfigsModelFactory:
    @staticmethod
    def get_patch_localized_configs(data: Data) -> PatchLocalizedConfigsModel:
        src_fields = {f.name: getattr(data, f.name) for f in fields(data)}
        dest_fields = {f.name for f in fields(PatchLocalizedConfigsModel)}

        init_kwargs = {
            field: src_fields[field] for field in dest_fields if field in src_fields
        }

        return PatchLocalizedConfigsModel(**init_kwargs)
