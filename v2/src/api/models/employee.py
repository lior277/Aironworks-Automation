# v2/src/api/models/employee.py
from typing import List

from pydantic import BaseModel, EmailStr


class EmployeeData(BaseModel):
    """Data model for creating employees"""

    first_name: str
    last_name: str
    email: EmailStr  # Validates email format!
    language: str = 'en'
    admin_role: bool = False
    employee_role: bool = True
    attack_vector_addresses: List[str] = []


class EmployeeResponse(BaseModel):
    """Response model from POST employee API"""

    id: int
    first_name: str
    last_name: str
    email: str
    language: str
    # Add other fields from actual response
