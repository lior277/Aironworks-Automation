import faker

from src.models.group.group_model import GroupModel
from src.utils.randomizer import ger_random_world, get_random_email

fake = faker.Faker()


class GroupModelFactory:
    @staticmethod
    def get_random_group() -> GroupModel:
        return GroupModel(
            name=ger_random_world(),
            admin_email=get_random_email(),
            admin_first_name=fake.first_name(),
            admin_last_name=fake.last_name(),
        )
