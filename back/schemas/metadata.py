from marshmallow import fields, Schema

class Metadata(Schema):
    _id = fields.UUID(required=True)
    name = fields.Str(required=True)
    _type = fields.Str(required=True)
    created = fields.Str(required=True, format='%Y-%m-%d %H:%M:%S')
    modified = fields.Str(required=False, , format='%Y-%m-%d %H:%M:%S')

{
   "@schemaLocation": "http://ltsc.ieee.org/xsd/LOM http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd",
   "general": {
      "identifier": {
         "catalog": "NBC",
         "entry": "07.10.01"
      },
      "title": "Nombre del Objeto",
      "language": "es",
      "description": "objeto",
      "keyword": [
         "objeto",
         "metadato"
      ],
      "coverage": "null",
      "structure": "null",
      "aggregationlevel": "null"
   },
   "lifecycle": {
      "version": "1",
      "status": "final",
      "contribute": {
         "role": "author",
         "date": "2013-02-27",
         "entity": "Valentina Tabares Morales"
      }
   },
   "metametadata": {
      "identifier": {
         "catalog": "URL",
         "entry": "http://www.ieee.org/descriptions/1234"
      },
      "contribute": {
         "role": "creator",
         "date": "2013-02-27",
         "entity": "Universidad Nacional de Colombia"
      },
      "metadataschema": "LOMv1.0",
      "language": "es"
   },
   "technical": {
      "format": "pdf",
      "size": "14117640",
      "location": "http://froac.manizales.unal.edu.co/roap/control/download.php?id=11",
      "requirements": {
         "orcomposite": {
            "type": "operating system",
            "name": "windows",
            "minimumversion": "win xp",
            "maximumversion": "win 8"
         }
      },
      "installationremarks": "No aplica",
      "otherplatformrequirements": "No aplica",
      "duration": "PT2M"
   },
   "educational": {
      "interactivitytype": "null",
      "learningresourcetype": "null",
      "interactivitylevel": "null",
      "semanticdensity": "null",
      "intendedenduserrole": "null",
      "context": "null",
      "typicalagerange": "null",
      "difficulty": "null",
      "typicallearningtime": "null",
      "description": "null",
      "language": "null"
   },
   "rights": {
      "cost": "no",
      "copyrightandotherrestrictions": "no",
      "description": "null"
   },
   "relation": {
      "kind": "ispartof",
      "resource": {
         "identifier": {
            "catalog": "URI",
            "entry": "http://www.louvre.org/video108"
         },
         "description": "Auditoria de Sistemas"
      }
   },
   "annotation": {
      "entity": "no aplica",
      "date": "2013-02-27",
      "description": "no aplica"
   },
   "classification": {
      "purpose": "educational objective",
      "taxonPath": {
         "source": "no aplica",
         "taxon": {
            "id": "no aplica",
            "entry": "no aplica"
         }
      },
      "description": "null",
      "keyword": "null"
   }
}