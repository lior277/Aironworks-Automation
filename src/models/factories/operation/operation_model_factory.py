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

    @staticmethod
    def get_operation_edit() -> OperationModel:
        return OperationModel(
            operation_name='Test 2 Operation 123#@!',
            campaign_name='Test 2 for Operation 123#@!',
        )
