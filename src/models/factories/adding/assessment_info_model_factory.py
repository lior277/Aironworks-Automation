from src.models.addin.assessment_info_model import AssessmentInfoModel, Config


class AssessmentInfoModelFactory:
    @classmethod
    def get_default_info(cls, soc_email: str) -> AssessmentInfoModel:
        return AssessmentInfoModel(
            soc_email=soc_email,
            config=Config(
                assessment_button=True,
                assessment_button_description='',
                assessment_button_text='Perform Assessment',
                incident_button=True,
                incident_button_description='',
                incident_button_text='Report an Incident',
                language='en',
                subtext='',
            ),
        )
