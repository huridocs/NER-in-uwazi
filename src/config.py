import os

USER = os.getenv("USER", "admin")
PASSWORD = os.getenv("PASSWORD", "admin")
URL = os.getenv("URL", "http://localhost:3000")
LANGUAGE = os.getenv("LANGUAGE", "en")
TEMPLATES = os.getenv("TEMPLATES", "5bfbb1a0471dd0fc16ada146").split(",")