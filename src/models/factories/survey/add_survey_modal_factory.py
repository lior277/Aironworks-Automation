from src.models.survey.add_survey_modal import AddSurveyModel, Model, Options


class AddSurveyModelFactory:
    @staticmethod
    def get_performance_survey() -> AddSurveyModel:
        options = [Options(text='Performance option 1')]
        return AddSurveyModel(
            survey_name='Performance survey',
            model=[Model(type='radio', options=options)],
        )
