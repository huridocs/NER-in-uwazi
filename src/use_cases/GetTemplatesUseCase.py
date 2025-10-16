from ner_in_docker.domain.NamedEntityType import NamedEntityType
from uwazi_api.UwaziAdapter import UwaziAdapter

from config import USER_NAME, PASSWORD, URL, LANGUAGES


class GetTemplatesUseCase:
    NAMES: dict[NamedEntityType, str] = {
        NamedEntityType.PERSON: 'Person',
        NamedEntityType.ORGANIZATION: 'Organization',
        NamedEntityType.LOCATION: 'Location',
        NamedEntityType.LAW: 'Law',
        NamedEntityType.DATE: 'Date',
        NamedEntityType.DOCUMENT_CODE: 'Reference Code'
    }

    RELATION_IDS: dict[NamedEntityType, str] = {
        NamedEntityType.PERSON: 'Person',
        NamedEntityType.ORGANIZATION: 'Organization',
        NamedEntityType.LOCATION: 'Location',
        NamedEntityType.LAW: 'Law',
        NamedEntityType.DATE: 'Date',
        NamedEntityType.DOCUMENT_CODE: 'Reference Code'
    }

    def __init__(self):
        self.uwazi_adapter = UwaziAdapter(user=USER_NAME, password=PASSWORD, url=URL)
        self.templates_by_type: dict[NamedEntityType, str] = dict()
        self.set_templates()

    def set_templates(self):
        templates = self.uwazi_adapter.templates.get()
        for template in templates:
            name = template['name']
            for ner_type, ner_name in self.NAMES.items():
                if name == ner_name:
                    self.templates_by_type[ner_type] = template['_id']
                    break

    def get(self, ner_type: NamedEntityType) -> str:
        if ner_type not in self.templates_by_type:
            self.create_template(ner_type)

        return self.templates_by_type[ner_type]

    @staticmethod
    def _create_property(prop_type: str, label: str) -> dict:
        return {
            "type": prop_type,
            "label": label,
            "noLabel": False,
            "required": False,
            "showInCard": False,
            "filter": False,
            "defaultfilter": False,
            "prioritySorting": False,
            "style": "",
            "generatedId": False
        }

    def _get_template_properties(self, ner_type: NamedEntityType) -> list[dict]:
        properties = []

        if ner_type == NamedEntityType.LOCATION:
            properties.append(self._create_property("geolocation", "Geolocation"))
        elif ner_type == NamedEntityType.DATE:
            properties.append(self._create_property("date", "Date"))

        return properties

    def create_template(self, ner_type: NamedEntityType):
        template_data = {
            "name": self.NAMES[ner_type],
            "color": "#628ccf",
            "properties": self._get_template_properties(ner_type),
            "commonProperties": [
                {"label": "Title", "name": "title", "type": "text", "isCommonProperty": True},
                {"label": "Date added", "name": "creationDate", "type": "date", "isCommonProperty": True},
                {"label": "Date modified", "name": "editDate", "type": "date", "isCommonProperty": True}
            ]
        }

        try:
            response = self.uwazi_adapter.templates.set(LANGUAGES[0], template_data)
        except Exception as e:
            print(f"Error creating template for {ner_type}: {e}")
            return False

        if response and '_id' in response:
            self.templates_by_type[ner_type] = response['_id']
            return True

        return False


if __name__ == '__main__':
    use_case = GetTemplatesUseCase()
    for ner_type in NamedEntityType:
        if ner_type != NamedEntityType.LOCATION:
            continue
        template_id = use_case.create_template(ner_type)
        print(f"Template for {ner_type.value}: {template_id}")
        break
