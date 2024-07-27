from src.models.education.clone_education_content import CloneEducationContentModel
from src.models.education.education_content_model import Item


class CloneEducationContentModelFactory:
    @staticmethod
    def get_education_content(item: Item) -> CloneEducationContentModel:
        return CloneEducationContentModel(
            any_company=item.any_company,
            description=item.description,
            level=item.level,
            parts=item.parts,
            title=item.title,
            topic_name=item.topic.name,
        )
