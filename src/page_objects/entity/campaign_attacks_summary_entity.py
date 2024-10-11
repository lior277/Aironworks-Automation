from datetime import datetime


class CampaignAttacksSummaryEntity:
    def __init__(
        self,
        status: str = None,
        opened: str = None,
        date_clicked: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        user_agent: str = None,
        ip_address: str = None,
        report_time: str = None,
        incident_time: str = None,
    ):
        self.status = status
        self.opened = opened
        self.date_clicked = date_clicked
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_agent = user_agent
        self.ip_address = ip_address
        self.report_time = report_time
        self.incident_time = incident_time

    def __eq__(self, other):
        if isinstance(other, CampaignAttacksSummaryEntity):
            return (
                self.status == other.status
                and self.opened == other.opened
                and self.date_clicked == other.date_clicked
                and self.first_name == other.first_name
                and self.last_name == other.last_name
                and self.email == other.email
                and self.user_agent == other.user_agent
                and self.ip_address == other.ip_address
                and self.report_time == other.report_time
                and self.incident_time == other.incident_time
            )
        return False

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class CampaignAttacksSummaryFactory:
    @staticmethod
    def get_entity_from_dict(row: dict) -> CampaignAttacksSummaryEntity:
        return CampaignAttacksSummaryEntity(
            status=row['Status'].title(),
            opened=bool_to_yes_no(row['Email Opened']),
            date_clicked=(
                datetime.strptime(row['Failure Date'], '%Y-%m-%d %H:%M:%S')
                .strftime('%-m/%-d/%Y %-I:%M %p')
                .lower()
                if row['Failure Date']
                else ''
            ),
            first_name=row['First Name'],
            last_name=row['Last Name'],
            email=row['Email'],
            user_agent=row['Device'],
            ip_address=row['IP Address'],
            report_time=row['Assessment Report Date'],
            incident_time=row['Incident Report Date'],
        )

    @staticmethod
    def get_entity(data: list[str]) -> CampaignAttacksSummaryEntity:
        return CampaignAttacksSummaryEntity(
            status=data[0],
            opened=data[1],
            date_clicked=data[2],
            first_name=data[3],
            last_name=data[4],
            email=data[5],
            user_agent=data[6],
            ip_address=data[7],
            report_time=data[8],
            incident_time=data[9],
        )


def bool_to_yes_no(bool_value: str) -> str:
    return 'Yes' if eval(bool_value) else 'No'
