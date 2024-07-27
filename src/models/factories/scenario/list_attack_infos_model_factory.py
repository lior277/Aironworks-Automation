from src.models.scenario.list_attack_infos_model import Filters, ListAttackInfosModel


class ListAttackInfosModelFactory:
    @staticmethod
    def get_list_attack_infos() -> ListAttackInfosModel:
        return ListAttackInfosModel(
            start_index=0, end_index=50, filters=[Filters(key='language', value='all')]
        )
