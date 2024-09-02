from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class GroupModel(BaseDataClass):
    name: str
    admin_email: str
    admin_first_name: str
    admin_last_name: str

    def to_csv_file(self):
        return {
            'Group Name': self.name,
            'Group Admin Email': self.admin_email,
            'Group Admin First Name': self.admin_first_name,
            'Group Admin Last Name': self.admin_last_name,
        }
