from time import sleep
import traceback

from uwazi_api.UwaziAdapter import UwaziAdapter

from config import USER_NAME, PASSWORD, URL, PDFS_FOLDER, TEMPLATES
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
                print("No more entities found. Exiting...")
                break

            print(f"Retrieved {len(entities)} entities starting from index {index}")
            for entity in entities:
                properties = self.get_uwazi_properties(entity)
                for uwazi_property in properties:
                    print(f"Processing entity {uwazi_property.identifier}")
                    named_entities_response = self.process_entity_use_case.get_ner_response(uwazi_property)
                    self.create_uwazi_entities_use_case.create_entities(uwazi_property, named_entities_response)
                    uwazi_property.remove_pdf()

            index += (self.BATCH_SIZE - self.OVERLAP)
            print(index)
            sleep(3)

    def get_uwazi_properties(self, entity: dict) -> list[UwaziProperty]:        
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