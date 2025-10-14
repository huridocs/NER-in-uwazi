from ner_in_docker.domain.NamedEntityType import NamedEntityType
from ner_in_docker.drivers.rest.response_entities.NamedEntitiesResponse import NamedEntitiesResponse

from domain.UwaziEntity import UwaziEntity
from use_cases.ProcessEntityUseCase import ProcessEntityUseCase


class TestProcessEntityUseCase:

    def setup_method(self):
        self.use_case = ProcessEntityUseCase()

    def test_get_ner_entities_with_person_organization_location(self):
        entity = UwaziEntity(
            identifier="test-doc-123",
            text="John Smith works at Microsoft in Seattle."
        )

        result = self.use_case.get_ner_entities(entity)

        assert result is not None
        assert isinstance(result, NamedEntitiesResponse)
        assert len(result.entities) > 0

        entity_texts = [e.text for e in result.entities]
        entity_labels = [e.type for e in result.entities]

        assert any("John Smith" in text or "Smith" in text for text in entity_texts)
        assert NamedEntityType.PERSON in entity_labels

    def test_get_ner_entities_with_document_code(self):
        entity = UwaziEntity(
            identifier="doc-456",
            text="The United Nations adopted resolution A/RES/60/1 in 2005."
        )

        result = self.use_case.get_ner_entities(entity)

        assert result is not None
        assert isinstance(result, NamedEntitiesResponse)
        assert len(result.entities) > 0

        entity_texts = [e.text for e in result.entities]
        assert any("A/RES/60/1" in text for text in entity_texts) or any("United Nations" in text for text in entity_texts)

    def test_get_ner_entities_with_law_reference(self):
        entity = UwaziEntity(
            identifier="doc-789",
            text="According to Article 5 of the Geneva Convention, all parties must comply."
        )

        result = self.use_case.get_ner_entities(entity)

        assert result is not None
        assert isinstance(result, NamedEntitiesResponse)

    def test_get_ner_entities_with_empty_text(self):
        entity = UwaziEntity(
            identifier="doc-empty",
            text=""
        )

        result = self.use_case.get_ner_entities(entity)

        assert result is not None
        assert isinstance(result, NamedEntitiesResponse)

    def test_get_ner_entities_with_complex_text(self):
        entity = UwaziEntity(
            identifier="doc-complex",
            text="On December 15, 2023, the European Union passed Regulation (EU) 2023/1234 "
                 "concerning data protection. Commissioner Jane Doe announced the decision in Brussels."
        )

        result = self.use_case.get_ner_entities(entity)

        assert result is not None
        assert isinstance(result, NamedEntitiesResponse)
        assert len(result.entities) > 0

