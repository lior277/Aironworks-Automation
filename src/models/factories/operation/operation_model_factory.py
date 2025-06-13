import faker

from src.models.operation_model import OperationModel

fake = faker.Faker()


class OperationModelFactory:
    @staticmethod
    def get_operation() -> OperationModel:
        return OperationModel(
            operation_name='Test Operation 123#@!',
            campaign_name='Test for Operation 123#@!',
        )
