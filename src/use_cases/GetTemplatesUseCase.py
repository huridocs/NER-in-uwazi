from uwazi_api.UwaziAdapter import UwaziAdapter

from config import USER, PASSWORD, URL
from domain.NamedEntityType import NamedEntityType


class GetTemplatesUseCase:
    def __init__(self):
        self.templates_by_type: dict[NamedEntityType, str] = dict()
        self.uwazi_adapter = UwaziAdapter(user=USER, password=PASSWORD, url=URL)
        self.set_templates()

    def set_templates(self):
        language = "en"
        templates = self.uwazi_adapter.templates.get(language)
        for template in templates:
            name = template['name']
            if name == 'Person':
                self.templates_by_type[NamedEntityType.PERSON] = template['_id']
            elif name == 'Organization':
                self.templates_by_type[NamedEntityType.ORGANIZATION] = template['_id']
            elif name == 'Location':
                self.templates_by_type[NamedEntityType.LOCATION] = template['_id']
            elif name == 'Law':
                self.templates_by_type[NamedEntityType.LAW] = template['_id']
            elif name == 'Date':
                self.templates_by_type[NamedEntityType.DATE] = template['_id']
            elif name == 'Reference Code':
                self.templates_by_type[NamedEntityType.DOCUMENT_CODE] = template['_id']


    def get(self, ner_type: NamedEntityType) -> str:
        if ner_type not in self.templates_by_type:
            self.set_templates()

        if ner_type not in self.templates_by_type:
            self.create_template(ner_type)

        self.set_templates()

        return self.templates_by_type[ner_type]

    def create_template(self, ner_type: NamedEntityType):
        pass