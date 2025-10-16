from ner_in_docker.domain.NamedEntityType import NamedEntityType
from ner_in_docker.drivers.rest.response_entities.GroupResponse import GroupResponse
from ner_in_docker.drivers.rest.response_entities.NamedEntitiesResponse import NamedEntitiesResponse
from uwazi_api.Reference import Reference, SelectionRectangle
from uwazi_api.UwaziAdapter import UwaziAdapter

from config import USER_NAME, PASSWORD, URL, LANGUAGES, TYPES_TO_PROCESS
from domain.UwaziGroups import UwaziGroups
from domain.UwaziProperty import UwaziProperty
from use_cases.GetTemplatesUseCase import GetTemplatesUseCase


class CreateUwaziEntitiesUseCase:
    BATCH_SIZE = 300

    RELATIONSHIP_IDS: dict[NamedEntityType, str] = {
        NamedEntityType.PERSON: '68f097910058648f7a83c2bf',
        NamedEntityType.ORGANIZATION: '68f0979d0058648f7a83c2d0',
        NamedEntityType.LOCATION: '68f097a60058648f7a83c2e5',
        NamedEntityType.LAW: '68f097ae0058648f7a83c2f6',
        NamedEntityType.DATE: '68f097b60058648f7a83c307',
        NamedEntityType.DOCUMENT_CODE: '68f097ce0058648f7a83c319'
    }

    def __init__(self):
        self.uwazi_adapter = UwaziAdapter(user=USER_NAME, password=PASSWORD, url=URL)
        self.get_templates_use_case = GetTemplatesUseCase()
        self.uwazi_groups = UwaziGroups()

    def create_entities(self, uwazi_property: UwaziProperty, named_entity_response: NamedEntitiesResponse):
        for group in named_entity_response.groups:
            if group.type not in TYPES_TO_PROCESS:
                continue
            template_id = self.get_templates_use_case.get(group.type)
            self.set_group_in_uwazi(template_id, group.type, group.group_name)

        for entity in named_entity_response.entities:
            if entity.type not in TYPES_TO_PROCESS:
                continue
            group_shared_id = self.uwazi_groups.get_group(entity.type, entity.group_name)
            reference = Reference(
                text=entity.text,
                selection_rectangles=[
                    SelectionRectangle(top=entity.segment.bounding_box.top / 0.75,
                                       left=entity.segment.bounding_box.left / 0.75,
                                       width=entity.segment.bounding_box.width / 0.75,
                                       height=entity.segment.bounding_box.height / 0.75,
                                       page=str(entity.segment.page_number)
                                       )])

            self.uwazi_adapter.relationships.create(
                file_entity_shared_id=uwazi_property.shared_id,
                file_id=uwazi_property.file_id,
                reference=reference,
                to_entity_shared_id=group_shared_id,
                relationship_type_id=self.RELATIONSHIP_IDS[entity.type],
                language=LANGUAGES[0])

            print(f"Created relationship for entity {entity.text} of type {entity.type} in document {uwazi_property.shared_id}")

    def set_group_in_uwazi(self, template_id: str, named_entity_type: NamedEntityType, group_name: str):
        if not self.uwazi_groups.get_group(group_type=named_entity_type, group_name=group_name):
            self.get_groups_from_uwazi(template_id, named_entity_type)

        if not self.uwazi_groups.get_group(group_type=named_entity_type, group_name=group_name):
            entity = {"metadata": {},
                      "template": template_id,
                      "title": group_name,
                      "type": "entity",
                      "documents": []}
            shared_id = self.uwazi_adapter.entities.upload(entity=entity, language=LANGUAGES[0])
            self.uwazi_groups.add_group(named_entity_type, group_name, shared_id)

    def create_group_in_uwazi(self, group_response: GroupResponse):
        pass

    def get_groups_from_uwazi(self, template_id: str, named_entity_type: NamedEntityType):
        index = 0
        while True:
            entities = self.uwazi_adapter.entities.get(start_from=index,
                                                       batch_size=self.BATCH_SIZE,
                                                       template_id=template_id)

            if not entities or len(entities) == 0:
                break

            for entity in entities:
                self.uwazi_groups.add_group(named_entity_type, entity.get('title', ''), entity.get('sharedId', ''))

            index += self.BATCH_SIZE
