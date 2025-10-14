from time import sleep

from uwazi_api.UwaziAdapter import UwaziAdapter

from use_cases.CreateUwaziEntitiesUseCase import CreateUwaziEntitiesUseCase


class ExtractNERUseCase:
    BATCH_SIZE = 300
    OVERLAP = 15

    def __init__(self):
        self.create_uwazi_entities_use_case = CreateUwaziEntitiesUseCase()

    def execute(self):
        index = 0
        while True:
            print("Looping entities...")
            uwazi_adapter = UwaziAdapter(user='admin', password='admin', url='http://localhost:3000')
            entities = uwazi_adapter.entities.get(start_from=index, batch_size=self.BATCH_SIZE)

            if not entities or len(entities) == 0:
                print("No more entities found. Exiting...")
                break

            print(f"Retrieved {len(entities)} entities starting from index {index}")
            print(entities)

            index += (self.BATCH_SIZE - self.OVERLAP)
            print(index)
            sleep(3)


if __name__ == '__main__':
    ExtractNERUseCase().execute()