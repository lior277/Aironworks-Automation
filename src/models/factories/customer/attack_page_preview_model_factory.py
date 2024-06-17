from src.models.customer.attack_page_preview_model import AttackPagePreviewModel


class AttackPagePreviewModelFactory:
    @staticmethod
    def get_education_campaign() -> AttackPagePreviewModel:
        return AttackPagePreviewModel(light_mode=True, show_survey_button=True)
