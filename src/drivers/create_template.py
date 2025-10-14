from uwazi_api.UwaziAdapter import UwaziAdapter


def create_template():
    language = "en"
    uwazi_adapter = UwaziAdapter(user='admin', password='admin', url='http://localhost:3000')
    template_dict = {"name": "foo_2", "color": "#C03B22", "entityViewPage": "", "properties": [],
             "commonProperties": [{"label": "Title", "name": "title", "type": "text", "isCommonProperty": True},
                                  {"label": "Date added", "name": "creationDate", "type": "date",
                                   "isCommonProperty": True},
                                  {"label": "Date modified", "name": "editDate", "type": "date",
                                   "isCommonProperty": True}]}
    template_dict = {"name": "foo_3"}
    uwazi_adapter.templates.set(language, template_dict)
    return True


if __name__ == '__main__':
    create_template()