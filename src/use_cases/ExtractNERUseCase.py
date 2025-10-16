import traceback

from uwazi_api.UwaziAdapter import UwaziAdapter

from config import USER_NAME, PASSWORD, URL, PDFS_FOLDER, TEMPLATES, PROPERTIES_TO_PROCESS
from domain.UwaziProperty import UwaziProperty
from use_cases.CreateUwaziEntitiesUseCase import CreateUwaziEntitiesUseCase
from use_cases.ProcessEntityUseCase import ProcessEntityUseCase

class ExtractNERUseCase:
    BATCH_SIZE = 300
    OVERLAP = 15

    def __init__(self):
        self.process_entity_use_case = ProcessEntityUseCase()
        self.create_uwazi_entities_use_case = CreateUwaziEntitiesUseCase()
        self.uwazi_adapter = UwaziAdapter(user=USER_NAME, password=PASSWORD, url=URL)

    def execute(self):
        index = 0
        while True:
            print("Looping entities...")
            entities = self.uwazi_adapter.entities.get(start_from=index, batch_size=self.BATCH_SIZE, template_id=TEMPLATES[0])

            if not entities or len(entities) == 0:
                print("No more entities found.")
                break

            print(f"Retrieved {len(entities)} entities starting from index {index}")
            for entity in entities:
                properties = self.get_text_properties(entity)
                properties.extend(self.get_documents_properties(entity))
                for uwazi_property in properties:
                    print(f"Processing entity {uwazi_property.identifier}")
                    named_entities_response = self.process_entity_use_case.get_ner_response(uwazi_property)
                    self.create_uwazi_entities_use_case.create_entities(uwazi_property, named_entities_response)
                    uwazi_property.remove_pdf()

            index += (self.BATCH_SIZE - self.OVERLAP)

    @staticmethod
    def get_text_properties(entity: dict) -> list[UwaziProperty]:
        properties = []

        if 'metadata' not in entity:
            return properties

        for metadata_key, metadata_value in entity['metadata'].items():
            if metadata_key not in PROPERTIES_TO_PROCESS:
                continue

            if not metadata_value or len(metadata_value) == 0:
                continue

            text = metadata_value[0].get('value', "")
            if not text:
                continue

            uwazi_property = UwaziProperty(
                shared_id=entity['sharedId'],
                content_hash=str(hash(text)),
                language=entity.get('language', 'en'),
                property_name=metadata_key,
                text=text
            )

            properties.append(uwazi_property)

        return properties


    def get_documents_properties(self, entity: dict) -> list[UwaziProperty]:
        properties = []
        
        if 'documents' not in entity:
            return properties
            
        for document in entity['documents']:
            if document.get('type') == 'document' and document.get('mimetype') == 'application/pdf':
                try:
                    pdf_filename = document.get('filename')
                    pdf_path = PDFS_FOLDER / pdf_filename

                    uwazi_property = UwaziProperty(
                        shared_id=entity['sharedId'],
                        content_hash=document.get('filename'),
                        language=entity.get('language', 'en'),
                        property_name=document.get('originalname', document.get('filename')),
                        pdf_path=pdf_path,
                        file_id=document.get('_id', None)
                    )

                    pdf_content = self.uwazi_adapter.files.get_document_by_file_name(pdf_filename)

                    if not pdf_content:
                        pdf_path.unlink(missing_ok=True)
                        continue

                    pdf_path.write_bytes(pdf_content)

                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_content)

                    properties.append(uwazi_property)
                    
                except Exception as e:
                    print(f"Error processing document {document['_id']}: {e}")
                    traceback.print_exc()
                    continue
        
        return properties


if __name__ == '__main__':
    ExtractNERUseCase().execute()