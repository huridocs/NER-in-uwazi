from uwazi_api.UwaziAdapter import UwaziAdapter


def create_entities():
    uwazi_adapter = UwaziAdapter(user='admin', password='admin', url='http://localhost:3000')
    for i in range(1000):
        uwazi_adapter.entities.upload({"metadata":{},"template":"5bfbb1a0471dd0fc16ada146","title":f"entity {i}","type":"entity","documents":[]}, "en")



if __name__ == '__main__':
    create_entities()