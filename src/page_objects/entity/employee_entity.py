from src.models.company.employee_list_model import EmployeeItemModel


class EmployeeEntity:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        language: str,
        mobile_number: str,
        linked_in: str,
        dial_code: str,
        facebook: str = None,
        twitter: str = None,
        instagram: str = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.language = language
        self.mobile_number = mobile_number
        self.linked_in = linked_in
        self.dial_code = dial_code
        self.facebook = facebook
        self.twitter = twitter
        self.instagram = instagram

    def __eq__(self, other):
        if isinstance(other, EmployeeEntity):
            return (
                self.first_name == other.first_name
                and self.last_name == other.last_name
                and self.email == other.email
                and self.language == other.language
                and self.mobile_number == other.mobile_number
                and self.dial_code == other.dial_code
                and self.linked_in == other.linked_in
                and self.facebook == other.facebook
                and self.twitter == other.twitter
                and self.instagram == other.instagram
            )
        return False

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class EmployeeEntityFactory:
    @staticmethod
    def from_employee_item(employee: EmployeeItemModel) -> EmployeeEntity:
        dial_code = next(
            (
                attack.value
                for attack in employee.attack_vector_addresses
                if attack.attack_vector == 'dial_code'
            ),
            None,
        )
        linked_in = next(
            (
                attack.value
                for attack in employee.attack_vector_addresses
                if attack.attack_vector == 'linkedin'
            ),
            None,
        )
        twitter = next(
            (
                attack.value
                for attack in employee.attack_vector_addresses
                if attack.attack_vector == 'twitter'
            ),
            None,
        )
        national_number = next(
            (
                attack.value
                for attack in employee.attack_vector_addresses
                if attack.attack_vector == 'national_number'
            ),
            None,
        )
        facebook = next(
            (
                attack.value
                for attack in employee.attack_vector_addresses
                if attack.attack_vector == 'facebook'
            ),
            None,
        )
        instagram = next(
            (
                attack.value
                for attack in employee.attack_vector_addresses
                if attack.attack_vector == 'instagram'
            ),
            None,
        )
        return EmployeeEntity(
            first_name=employee.first_name,
            last_name=employee.last_name,
            language=employee.language,
            email=employee.email,
            linked_in=linked_in,
            mobile_number=national_number,
            twitter=twitter,
            dial_code=dial_code,
            facebook=facebook,
            instagram=instagram,
        )

    @staticmethod
    def get_entity_from_dict(row: list[str]) -> EmployeeEntity:
        return EmployeeEntity(
            first_name=row[0],
            last_name=row[1],
            email=row[2],
            language=row[3],
            linked_in=row[4],
            twitter=row[5],
            dial_code=row[6],
            instagram=row[7],
            mobile_number=row[8],
            facebook=row[9],
        )
