from enum import StrEnum


class NamedEntityType(StrEnum):
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    DATE = "DATE"
    LAW = "LAW"
    DOCUMENT_CODE = "DOCUMENT_CODE"
    REFERENCE = "REFERENCE"
