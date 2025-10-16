import os
from pathlib import Path

from PIL.TiffTags import TYPES
from ner_in_docker.domain.NamedEntityType import NamedEntityType

ROOT_FOLDER = Path(__file__).parent.parent
PDFS_FOLDER = ROOT_FOLDER / "pdfs"

USER_NAME = os.getenv("USER_NAME", "admin")
PASSWORD = os.getenv("PASSWORD", "admin")
URL = os.getenv("URL", "http://localhost:3000")
LANGUAGES = os.getenv("LANGUAGE", "en").split(",")
TEMPLATES = os.getenv("TEMPLATES", "5bfbb1a0471dd0fc16ada146").split(",")
NAMESPACE = os.getenv("NAMESPACE", "default")

TYPES_TO_PROCESS = [
    NamedEntityType.PERSON,
    NamedEntityType.ORGANIZATION,
    NamedEntityType.LOCATION,
    NamedEntityType.LAW,
    NamedEntityType.DATE,
    NamedEntityType.DOCUMENT_CODE
]

NER_IN_DOCKER_URL = os.getenv("NER_IN_DOCKER_URL", "http://localhost")
NER_IN_DOCKER_PORT = os.getenv("NER_IN_DOCKER_PORT", "5070")