from ner_in_docker.domain.BoundingBox import BoundingBox
from ner_in_docker.domain.NamedEntityType import NamedEntityType
from ner_in_docker.drivers.rest.response_entities.EntityTextResponse import EntityTextResponse
from ner_in_docker.drivers.rest.response_entities.GroupResponse import GroupResponse
from ner_in_docker.drivers.rest.response_entities.NamedEntitiesResponse import NamedEntitiesResponse
from ner_in_docker.drivers.rest.response_entities.NamedEntityResponse import NamedEntityResponse
from ner_in_docker.drivers.rest.response_entities.SegmentResponse import SegmentResponse
from uwazi_api.UwaziAdapter import UwaziAdapter

from config import USER_NAME, PASSWORD, URL, LANGUAGES
from domain.UwaziGroups import UwaziGroups
from use_cases.GetTemplatesUseCase import GetTemplatesUseCase


class CreateUwaziEntitiesUseCase:
    BATCH_SIZE = 300

    def __init__(self):
        self.uwazi_adapter = UwaziAdapter(user=USER_NAME, password=PASSWORD, url=URL)
        self.get_templates_use_case = GetTemplatesUseCase()
        self.uwazi_groups = UwaziGroups()

    def create_entities(self, named_entity_response: NamedEntitiesResponse):
        for group in named_entity_response.groups:
            template_id = self.get_templates_use_case.get(group.type)
            self.set_group_in_uwazi(template_id, group.type, group.group_name)

        print(f"Groups: \n {self.uwazi_groups}")

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


if __name__ == '__main__':
    example = NamedEntitiesResponse(
        entities=[
            NamedEntityResponse(
                group_name='Héctor Fix-Zamudio',
                type=NamedEntityType.PERSON,
                text='Héctor Fix-Zamudio',
                character_start=0,
                character_end=18,
                relevance_percentage=21,
                segment=SegmentResponse(
                    text='Héctor Fix-Zamudio Presidente',
                    page_number=2,
                    segment_number=19,
                    character_start=0,
                    character_end=18,
                    bounding_box=BoundingBox(left=248, top=201, width=99, height=22),
                    pdf_name='file'
                ),
                source_id='file'
            )
        ],
        groups=[
            GroupResponse(
                group_name='Héctor Fix-Zamudio',
                type=NamedEntityType.PERSON,
                entities=[
                    EntityTextResponse(index=0, text='Héctor Fix-Zamudio')
                ],
                top_relevance_entity=NamedEntityResponse(
                    group_name='Héctor Fix-Zamudio',
                    type=NamedEntityType.PERSON,
                    text='Héctor Fix-Zamudio',
                    character_start=0,
                    character_end=18,
                    relevance_percentage=21,
                    segment=SegmentResponse(
                        text='Héctor Fix-Zamudio Presidente',
                        page_number=2,
                        segment_number=19,
                        character_start=0,
                        character_end=18,
                        bounding_box=BoundingBox(left=248, top=201, width=99, height=22),
                        pdf_name='file'
                    ),
                    source_id='file'
                )
            )
        ]
    )
    CreateUwaziEntitiesUseCase().create_entities(example)