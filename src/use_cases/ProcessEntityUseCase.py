import requests
from ner_in_docker.drivers.rest.response_entities.NamedEntitiesResponse import NamedEntitiesResponse

from src.domain.UwaziProperty import UwaziProperty
from config import NER_IN_DOCKER_URL, NER_IN_DOCKER_PORT, NAMESPACE


class ProcessEntityUseCase:

    def __init__(self):
        self.ner_url = f"{NER_IN_DOCKER_URL}:{NER_IN_DOCKER_PORT}/"

    def get_ner_response(self, uwazi_property: UwaziProperty) -> NamedEntitiesResponse | None:
        form_data = {
            "namespace": NAMESPACE,
            "identifier": uwazi_property.identifier,
            "text": uwazi_property.text if hasattr(uwazi_property, 'text') else None,
            "fast": False
        }

        files = None
        if uwazi_property.pdf_path:
            with open(uwazi_property.pdf_path, 'rb') as f:
                files = {"file": f.read()}

        try:
            response = requests.post(self.ner_url, data=form_data, files=files)
            response.raise_for_status()

            response_data = response.json()
            return NamedEntitiesResponse(**response_data)
        except requests.exceptions.RequestException as e:
            print(f"Error calling NER service: {e}")
            return None
        except Exception as e:
            print(f"Error processing NER response: {e}")
            return None


    def is_property_processed(self, uwazi_property: UwaziProperty) -> bool:
        ner_url = f"{self.ner_url}is_processed"

        form_data = {
            "namespace": NAMESPACE,
            "identifier": uwazi_property.identifier
        }

        try:
            response = requests.post(ner_url, data=form_data)
            response.raise_for_status()

            response_data = response.json()
            return response_data == True
        except requests.exceptions.RequestException as e:
            print(f"Error calling is_processed service: {e}")
            return False
        except Exception as e:
            print(f"Error processing is_processed response: {e}")
            return False


if __name__ == '__main__':
    ProcessEntityUseCase()