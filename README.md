# NER-in-uwazi

    [x] How to create references
        [x] entity to entity ?
        [x] PDF to entity ?
        [x] Paragraph to entity ?
        [x] Text selection to entity ?
    [x] Can the uwazi adapter create templates?
    [x] How to loop entities in uwazi
        [x] Save entities already processed
    [x] Add endpoint in NER-in-docker to check if a entity is already processed
        [-] Save the last timestamp processed
    [x] Identifier
        [x] shared_id language property_name MD5
    [x] Loop entities
    [x] Create templates for the different entities types
        [x] PERSON = "PERSON"
        [x] ORGANIZATION = "ORGANIZATION"
        [x] LOCATION = "LOCATION"
        [x] DATE = "DATE"
        [x] LAW = "LAW"
        [x] DOCUMENT_CODE = "DOCUMENT_CODE"
    [x] Query NER-in-docker
    [x] Get documents
    [x] Query NER-in-docker with PDF
    [x] Check if group exist in Uwazi
        [x] Create uwazi entity regarding the group if does not exist
    [x] Create connection   
        [x] divide possitions by 0.75
    [x] Check why dates are not standard??
    [x] Get selection by words not by segment
    [x] NER-in-docker does not normalice some dates text because other languages an so
    [x] Add references for text properties
    [x] Check if entity already processed
    [x] Create new entities for the text and PDF appearances
    [x] Link entities to each other
        [x] Create relationships for each NER type
        [x] Create relation property in templates
    [x] Download PDF and process them
    [x] Create text references
    [x] Get selection by words not by segment
        [x] Use PDFFeatures for that matter
    [x] Use pdf-features in NER-in-docker
    [x] Avoid loading group entities every time a group should be created
    [x] Check if references are already created
    [ ] Improve bounding boxes accuracy
        [ ] two lines text are not handled properly for the bounding box
    [ ] Improve processing speed
        [ ] With boxes 118s
        [ ] Without 111s
    [ ] Get right the languages used
    [ ] Document code in NER-in-docker is not working
    [ ] Skip entities with relationships
    [ ] Errors 
        [ ] Error setting relationships 422 {"error":"validation failed","validations":[{"instancePath":"/1/entity","schemaPath":"#/items/properties/entity/type","keyword":"type","params":{"type":"string"},"message":"must be string"}],"logLevel":"debug","prettyMessage":"validation failed\n/1/entity: must be string","requestId":8308}
        [ ] Some references are linked to two different relations
        [ ] Ner service says 2025-10-20 11:29:58,768 Warning: An empty Sentence was created! Are there empty strings in your dataset?
    [ ] Fulfill custom fields like
        [ ] Geolocalozation
            [ ] Secondary loop for filling the Geolocalization data
        [ ] Date


Create reference:

{
  "delete": [],
  "save": [
    [
      {
        "entity": "0mg4pkm4y78n",
        "template": null,
        "reference": {
          "text": "29 DE JULIO DE 1991",
          "selectionRectangles": [
            {
              "top": 172.94667742693863,
              "left": 335.66813738787613,
              "width": 155.3464233398437,
              "height": 17.629629629629626,
              "page": "1"
            }
          ]
        },
        "file": "68f098050058648f7a83c35f"
      },
      {
        "entity": "cos3av69d98",
        "template": "68f097b60058648f7a83c307"
      }
    ]
  ]
}



import requests

cookies = {
    'locale': 'en',
    '_pk_id.1.1fff': '7422e55bd6924caa.1759739219.',
    'connect.sid': 's%3A6Z05kDJRaW29W6-q5TXqcV5ano4AycFF.pKqEqZB%2B2AbCASUyhJQTyABl8Qs0Otld6nSjucNpSIE',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Language': 'en',
    'Origin': 'http://localhost:3000',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'locale=en; _pk_id.1.1fff=7422e55bd6924caa.1759739219.; connect.sid=s%3A6Z05kDJRaW29W6-q5TXqcV5ano4AycFF.pKqEqZB%2B2AbCASUyhJQTyABl8Qs0Otld6nSjucNpSIE',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
}

json_data = {
    'delete': [],
    'save': [
        [
            {
                'entity': '0mg4pkm4y78n',
                'template': None,
                'reference': {
                    'text': '29 DE JULIO DE 1991',
                    'selectionRectangles': [
                        {
                            'top': 172.94667742693863,
                            'left': 335.66813738787613,
                            'width': 155.3464233398437,
                            'height': 17.629629629629626,
                            'page': '1',
                        },
                    ],
                },
                'file': '68f098050058648f7a83c35f',
            },
            {
                'entity': 'cos3av69d98',
                'template': '68f097b60058648f7a83c307',
            },
        ],
    ],
}

response = requests.post('http://localhost:3000/api/relationships/bulk', cookies=cookies, headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"delete":[],"save":[[{"entity":"0mg4pkm4y78n","template":null,"reference":{"text":"29 DE JULIO DE 1991","selectionRectangles":[{"top":172.94667742693863,"left":335.66813738787613,"width":155.3464233398437,"height":17.629629629629626,"page":"1"}]},"file":"68f098050058648f7a83c35f"},{"entity":"cos3av69d98","template":"68f097b60058648f7a83c307"}]]}'
#response = requests.post('http://localhost:3000/api/relationships/bulk', cookies=cookies, headers=headers, data=data)


