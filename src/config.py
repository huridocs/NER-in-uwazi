import os

USER_NAME = os.getenv("USER_NAME", "admin")
PASSWORD = os.getenv("PASSWORD", "admin")
URL = os.getenv("URL", "http://localhost:3000")
LANGUAGES = os.getenv("LANGUAGE", "en").split(",")
TEMPLATES = os.getenv("TEMPLATES", "5bfbb1a0471dd0fc16ada146").split(",")
NAMESPACE = os.getenv("NAMESPACE", "default")


NER_IN_DOCKER_URL = os.getenv("NER_IN_DOCKER_URL", "http://localhost")
NER_IN_DOCKER_PORT = os.getenv("NER_IN_DOCKER_PORT", "5070")