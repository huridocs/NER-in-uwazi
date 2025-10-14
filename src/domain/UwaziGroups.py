from ner_in_docker.domain.NamedEntityType import NamedEntityType
from pydantic import BaseModel

from domain.UwaziGroupKey import UwaziGroupKey


class UwaziGroups(BaseModel):
    uwazi_groups: dict[UwaziGroupKey, str] = dict()

    def add_group(self, group_type: NamedEntityType, group_name: str):
        key = UwaziGroupKey(type=group_type, group_name=group_name)
        if key not in self.uwazi_groups:
            self.uwazi_groups[key] = group_name

    def get_group(self, group_type: NamedEntityType, group_name: str) -> str | None:
        key = UwaziGroupKey(type=group_type, group_name=group_name)
        return self.uwazi_groups.get(key)
