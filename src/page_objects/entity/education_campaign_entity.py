from src.models.education.education_campaign_model import EducationCampaignDetailsModel
from src.utils.date_util import timestamp_to_time


class EducationCampaignEntity:
    def __init__(self, title: str = None, assignments_submission_rate: str = None, start_date: str = None,
                 end_date: str = None, assignments_count: int = None, company_name: str = None):
        self.title = title
        self.assignments_submission_rate = assignments_submission_rate
        self.start_date = start_date
        self.end_date = end_date
        self.assignments_count = assignments_count
        self.company_name = company_name

    def __eq__(self, other):
        if isinstance(other, EducationCampaignEntity):
            return (self.title == other.title and
                    self.assignments_submission_rate == other.assignments_submission_rate and
                    self.start_date == other.start_date and self.end_date == other.end_date and
                    self.assignments_count == other.assignments_count and self.company_name == other.company_name)
        return False

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class EducationCampaignFactory:

    @staticmethod
    def get_education_campaign(education_campaign: EducationCampaignDetailsModel) -> EducationCampaignEntity:
        "Completion count / Number of campaign targets * 100%. Format and precision: 49%"
        rate = f"{int(education_campaign.assignments_submission_rate)}% ({int(education_campaign.assignments_submitted)}/{education_campaign.assignments_count})"
        return EducationCampaignEntity(title=education_campaign.title,
                                       assignments_submission_rate=rate,
                                       start_date=timestamp_to_time(education_campaign.start_date),
                                       end_date=timestamp_to_time(education_campaign.end_date),
                                       assignments_count=education_campaign.assignments_count,
                                       company_name=education_campaign.company.name if education_campaign.company else None)
