from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class EmployeeModel(BaseDataClass):
    email: str
    first_name: str
    last_name: str
    employee_id: Optional[int] = None

    def to_csv_file(self):
        return {
            'Email': self.email,
            'First Name': self.first_name,
            'Last Name': self.last_name,
        }
