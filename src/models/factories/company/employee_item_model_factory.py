import faker

from src.models.company.employee_list_model import AttackVectorModel, EmployeeItemModel
from src.utils.randomizer import get_random_email

fake = faker.Faker()


class EmployeeItemModelFactory:
    @staticmethod
    def get_random_employee() -> EmployeeItemModel:
        first_name = fake.first_name()
        last_name = fake.last_name()
        attack_vectors = [
            AttackVectorModel(attack_vector='dial_code', value='+44'),
            AttackVectorModel(
                attack_vector='national_number', value=fake.numerify('###-###-####')
            ),
            AttackVectorModel(
                attack_vector='facebook', value=f'https://facebook.com/{first_name}'
            ),
            AttackVectorModel(
                attack_vector='twitter', value=f'https://twitter.com/{first_name}'
            ),
            AttackVectorModel(
                attack_vector='linkedin', value=f'https://linkedin.com/in/{first_name}'
            ),
            AttackVectorModel(
                attack_vector='instagram', value=f'https://instagram.com/{first_name}'
            ),
        ]
        return EmployeeItemModel(
            first_name=first_name,
            last_name=last_name,
            email=get_random_email(),
            admin_role=False,
            attack_vector_addresses=attack_vectors,
            employee_role=True,
            fields=[],
            full_name=f'{first_name} {last_name}',
            id=None,
            language='English',
        )
