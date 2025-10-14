from time import sleep

from uwazi_api.UwaziAdapter import UwaziAdapter
from domain.UwaziEntity import UwaziEntity


def loop_entities():
    a = UwaziEntity(identifier="1")
    print(a)
    index = 1000
    while True:
        print("Looping entities...")
        uwazi_adapter = UwaziAdapter(user='admin', password='admin', url='http://localhost:3000')
        entities = uwazi_adapter.entities.get(start_from=index, batch_size=1)
        index += 1
        print(entities)
        sleep(3)


if __name__ == '__main__':
    loop_entities()