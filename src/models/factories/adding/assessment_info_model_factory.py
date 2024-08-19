from src.models.addin.assessment_info_model import AssessmentInfoModel, Config


class AssessmentInfoModelFactory:
    @classmethod
    def get_default_info(cls, soc_email: str) -> AssessmentInfoModel:
        return AssessmentInfoModel(
            soc_email=soc_email,
            config=Config(
                assessment_button=True,
                assessment_button_description="Click the above button to evaluate the email's security level and get risk assessment result",
                assessment_button_text='Perform AI Risk Assessment',
                incident_button=True,
                incident_button_description="Click the above button in case you entered a suspicious link or downloaded a suspicious file and forward the email to your organization's security center and allow them to conduct further investigation to assess the situation's risk level",
                incident_button_text='Report an Incident',
                language='en',
                subtext='',
            ),
        )
