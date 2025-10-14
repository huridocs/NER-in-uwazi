from ner_in_docker.domain.NamedEntityType import NamedEntityType
from pydantic import BaseModel


class UwaziGroupKey(BaseModel):
    type: NamedEntityType
    group_name: str
    __hash__ = lambda self: hash((self.type, self.group_name))