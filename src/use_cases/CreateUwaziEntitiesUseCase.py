from ner_in_docker.drivers.rest.response_entities.GroupResponse import GroupResponse
from ner_in_docker.drivers.rest.response_entities.NamedEntitiesResponse import NamedEntitiesResponse
from uwazi_api.UwaziAdapter import UwaziAdapter

from config import USER_NAME, PASSWORD, URL
from domain.UwaziGroups import UwaziGroups
from use_cases.GetTemplatesUseCase import GetTemplatesUseCase


class CreateUwaziEntitiesUseCase:
    def __init__(self):
        self.uwazi_adapter = UwaziAdapter(user=USER_NAME, password=PASSWORD, url=URL)
        self.get_templates_use_case = GetTemplatesUseCase()
        self.uwazi_groups = UwaziGroups()

    def create_entities(self, named_entity_response: NamedEntitiesResponse):
        pass

    def exist_group_in_uwazi(self, group_response: GroupResponse) -> bool:
        pass

    def create_group_in_uwazi(self, group_response: GroupResponse):
        pass
