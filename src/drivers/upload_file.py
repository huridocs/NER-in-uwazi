from uwazi_api.UwaziAdapter import UwaziAdapter


def upload_file(pdf_file_path, name):
    language = "en"

    if language not in ['en']:
        print(language)
        return False

    uwazi_adapter = UwaziAdapter(user='admin', password='admin', url='http://localhost:3000')
    entity = {"title": name, "template": "5bfbb1a0471dd0fc16ada146"}
    uwazi_adapter.entities.upload(entity, "en")
    shared_id = uwazi_adapter.entities.upload(entity, "en")
    uwazi_adapter.files.upload_file(pdf_file_path, shared_id, language, name)
    return True


if __name__ == '__main__':
    upload_file("/src/regular.pdf", "regular")