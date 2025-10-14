class ProcessEntityUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, entity):
        # Business logic to process the entity
        processed_entity = self._process(entity)
        self.repository.save(processed_entity)
        return processed_entity

    def _process(self, entity):
        # Placeholder for actual processing logic
        entity['processed'] = True
        return entity