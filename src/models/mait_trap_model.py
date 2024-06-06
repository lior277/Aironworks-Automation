from dataclasses import dataclass

from src.configs.config_loader import AppConfigs
from src.models.base_dataclass import BaseDataClass


@dataclass
class MailTrapModel(BaseDataClass):
    email: str
    id: str


class MailTrapModelFactory:
    @staticmethod
    def get_perf_mail_trap_inboxes() -> list[MailTrapModel]:
        return [MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_1, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_1),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_2, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_2),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_3, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_3),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_4, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_4),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_5, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_5),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_6, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_6),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_7, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_7),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_8, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_8),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_9, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_9),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_10, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_10),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_11, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_11),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_12, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_12),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_13, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_13),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_14, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_14),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_15, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_15),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_16, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_16),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_17, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_17),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_18, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_18),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_19, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_19),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_20, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_20),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_21, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_21),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_22, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_22),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_23, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_23),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_24, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_24),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_25, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_25),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_26, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_26),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_27, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_27),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_28, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_28),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_29, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_29),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_30, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_30),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_31, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_31),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_32, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_32),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_33, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_33),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_34, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_34),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_35, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_35),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_36, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_36),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_37, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_37),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_38, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_38),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_39, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_39),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_40, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_40),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_41, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_41),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_42, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_42),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_43, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_43),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_44, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_44),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_45, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_45),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_46, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_46),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_47, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_47),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_48, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_48),
                MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX_49, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID_49)]

    @staticmethod
    def get_perf_mail_trap_inbox() -> MailTrapModel:
        return MailTrapModel(email=AppConfigs.PERF_EMPLOYEE_INBOX, id=AppConfigs.PERF_EMPLOYEE_INBOX_ID)
