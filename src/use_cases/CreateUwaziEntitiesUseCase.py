from ner_in_docker.domain.NamedEntityType import NamedEntityType
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
        self._loaded_types = set()

    def create_entities_from_text(self, uwazi_property: UwaziProperty, named_entity_response: NamedEntitiesResponse):
        if not uwazi_property.text:
            return

        for entity in named_entity_response.entities:
            if entity.type not in TYPES_TO_PROCESS:
                continue

            group_shared_id = self.uwazi_groups.get_group(entity.type, entity.group_name)
            uwazi_entity = self.uwazi_adapter.entities.get_one(group_shared_id, language=LANGUAGES[0])
            if not uwazi_entity:
                continue

            reference_key = f'{str(entity.type).lower()}_references'

            metadata = uwazi_entity.get('metadata', {})
            relationships = metadata.get(reference_key, [])
            relationships.append({
                "value": uwazi_property.shared_id,
            })

            metadata[reference_key] = relationships
            uwazi_entity['metadata'] = metadata
            self.uwazi_adapter.entities.upload(uwazi_entity, LANGUAGES[0])
            print(f"Created relationship [{entity.type}] {entity.text} // {uwazi_property.shared_id}")

    def create_entities_from_pdf(self, uwazi_property: UwaziProperty, named_entity_response: NamedEntitiesResponse):
        for entity in named_entity_response.entities:
            if entity.type not in TYPES_TO_PROCESS:
                continue
            group_shared_id = self.uwazi_groups.get_group(entity.type, entity.group_name)
            selection_rectangles = []
            for text_position in entity.text_positions:
                selection_rectangles.append(
                    SelectionRectangle(top=text_position.top / 0.75,
                                       left=text_position.left / 0.75,
                                       width=text_position.width / 0.75,
                                       height=text_position.height / 0.75,
                                       page=str(entity.segment.page_number)
                                       ))
            reference = Reference(
                text=entity.text,
                selection_rectangles=selection_rectangles)

            self.uwazi_adapter.relationships.create(
                file_entity_shared_id=uwazi_property.shared_id,
                file_id=uwazi_property.file_id,
                reference=reference,
                to_entity_shared_id=group_shared_id,
                relationship_type_id=self.RELATIONSHIP_IDS[entity.type],
                language=LANGUAGES[0])

            print(f"Created relationship [{entity.type}] {entity.text} // {uwazi_property.shared_id}")

    def create_entities(self, uwazi_property: UwaziProperty, named_entity_response: NamedEntitiesResponse):
        for group in named_entity_response.groups:
            if group.type not in TYPES_TO_PROCESS:
                continue
            template_id = self.get_templates_use_case.get(group.type)
            self.set_group_in_uwazi(template_id, group.type, group.group_name)

        if not uwazi_property.file_id:
            self.create_entities_from_text(uwazi_property, named_entity_response)
        else:
            self.create_entities_from_pdf(uwazi_property, named_entity_response)

    def set_group_in_uwazi(self, template_id: str, named_entity_type: NamedEntityType, group_name: str):
        if not self.uwazi_groups.get_group(group_type=named_entity_type, group_name=group_name):
            if named_entity_type not in self._loaded_types:
                self._load_all_groups_for_type(template_id, named_entity_type)
                self._loaded_types.add(named_entity_type)
            else:
                self._search_group_by_name(template_id, named_entity_type, group_name)

        if not self.uwazi_groups.get_group(group_type=named_entity_type, group_name=group_name):
            entity = {"metadata": {},
                      "template": template_id,
                      "title": group_name,
                      "type": "entity",
                      "documents": []}
            shared_id = self.uwazi_adapter.entities.upload(entity=entity, language=LANGUAGES[0])
            self.uwazi_groups.add_group(named_entity_type, group_name, shared_id)

    def _search_group_by_name(self, template_id: str, named_entity_type: NamedEntityType, group_name: str):
        entities = self.uwazi_adapter.entities.get_from_text(
            search_term=group_name,
            template_id=template_id,
            batch_size=300,
            language=LANGUAGES[0]
        )

        for entity in entities:
            if entity.get('title', '') == group_name:
                self.uwazi_groups.add_group(named_entity_type, group_name, entity.get('sharedId', ''))
                break

    def _load_all_groups_for_type(self, template_id: str, named_entity_type: NamedEntityType):
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

    def get_groups_from_uwazi(self, template_id: str, named_entity_type: NamedEntityType):
        self._load_all_groups_for_type(template_id, named_entity_type)
