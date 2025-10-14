import requests
from drivers.rest.response_entities.NamedEntitiesResponse import NamedEntitiesResponse

from domain.UwaziEntity import UwaziEntity
from config import NER_IN_DOCKER_URL, NER_IN_DOCKER_PORT, NAMESPACE


class ProcessEntityUseCase:
    def get_ner_entities(self, entity: UwaziEntity) -> NamedEntitiesResponse | None:
        ner_url = f"{NER_IN_DOCKER_URL}:{NER_IN_DOCKER_PORT}/"

        form_data = {
            "namespace": NAMESPACE,
            "identifier": entity.identifier,
            "text": entity.text if hasattr(entity, 'text') else None,
            "fast": False
        }

        files = None
        if entity.pdf_path:
            files = {"file": entity.pdf_path}

        try:
            response = requests.post(ner_url, data=form_data, files=files)
            response.raise_for_status()

            response_data = response.json()
            return NamedEntitiesResponse(**response_data)
        except requests.exceptions.RequestException as e:
            print(f"Error calling NER service: {e}")
            return None
        except Exception as e:
            print(f"Error processing NER response: {e}")
            return None

if __name__ == '__main__':
    ProcessEntityUseCase()