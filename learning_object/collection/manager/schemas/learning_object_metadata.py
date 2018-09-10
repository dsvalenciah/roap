
"""
Contains utility functions to works with learning-object and his metadata
fields schemas.
"""

# TODO: to add many nested fields, add many=True in all nested fields
# handle it with @predump and add the multiple forms in the front end

from marshmallow import Schema, fields, validate, pre_dump

class Identifier(Schema):
    catalog = fields.String(required=True)
    entry = fields.String(required=True)

class General(Schema):
    identifier = fields.Nested(Identifier)  # Must be many=True
    title = fields.String(required=True)
    language = fields.List(fields.String(), required=True)
    description = fields.List(fields.String(), required=True)
    keyword = fields.List(fields.String(), required=True)
    coverage = fields.List(fields.String(), required=True)
    structure = fields.String(required=True)
    aggregationlevel = fields.String(
        required=True,
        validate=validate.OneOf(["1", "2", "3", "4"])
    )
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['identifier']) is dict:
    #        indata['identifier'] = [indata['identifier']] 

class Contribute(Schema):
    role = fields.String(required=True)
    date = fields.DateTime(required=True)
    entity = fields.List(fields.String(), required=True)

class LifeCycle(Schema):
    version = fields.String(required=True)
    status = fields.String(required=True)
    contribute = fields.List(fields.String(), required=True)

class MetaMetadata(Schema):
    identifier = fields.Nested(Identifier)  # Must be many=True
    contribute = fields.Nested(Contribute)  # Must be many=True
    metadataschema = fields.String(required=True)
    language = fields.List(fields.String(), required=True)
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['identifier']) is dict:
    #        indata['identifier'] = [indata['identifier']]
    #    if type(indata['contribute']) is dict:
    #        indata['contribute'] = [indata['contribute']]

class Orcomposite(Schema):
    type = fields.String(required=True)
    name = fields.String(required=True)
    minimumversion = fields.String(required=True)
    maximumversion = fields.String(required=True)

class Requirements(Schema):
    orcomposite = fields.Nested(Orcomposite)  # Must be many=True
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['orcomposite']) is dict:
    #        indata['orcomposite'] = [indata['orcomposite']] 

class Technical(Schema):
    format = fields.List(fields.String(), required=True)
    size =  fields.String(required=True)
    location = fields.List(fields.String(), required=True)
    requirements = fields.Nested(Requirements)  # Must be many=True
    installationremarks = fields.List(fields.String(), required=True)
    otherplatformrequirements = fields.List(fields.String(), required=True)
    duration =  fields.String(required=True)
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['requirements']) is dict:
    #        indata['requirements'] = [indata['requirements']] 

class Educational(Schema):
    interactivitytype = fields.String(required=True)
    learningresourcetype = fields.List(fields.String(), required=True)
    interactivitylevel = fields.String(
        required=True,
        validate=validate.OneOf(["active", "expositive", "mixed"])
    )
    semanticdensity = fields.String(
        required=True,
        validate=validate.OneOf(
            ["very low", "low", "medium", "high", "very high"]
        )
    )
    intendedenduserrole = fields.List(fields.String(), required=True)
    context = fields.List(fields.String(), required=True)
    typicalagerange = fields.List(fields.String(), required=True)
    difficulty = fields.String(
        required=True,
        validate=validate.OneOf(
            ["very easy", "easy", "medium", "difficult", "very difficult"]
        )
    )
    typicallearningtime = fields.String(required=True)
    description = fields.List(fields.String(), required=True)
    language = fields.List(fields.String(), required=True)

class Rights(Schema):
    cost = fields.String(required=True)
    copyrightandotherrestrictions = fields.String(required=True)
    description = fields.String(required=True)

class Resource(Schema):
    identifier = fields.Nested(Identifier)  # Must be many=True
    description = fields.List(fields.String(), required=True)
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['identifier']) is dict:
    #        indata['identifier'] = [indata['identifier']] 

class Relation(Schema):
    kind = fields.String(required=True)
    resource = fields.Nested(Resource)  # Must be many=True
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['resource']) is dict:
    #        indata['resource'] = [indata['resource']] 

class Annotation(Schema):
    entity = fields.String(required=True)
    date = fields.DateTime(required=True)
    description = fields.String(required=True)

class Taxon(Schema):
    id = fields.String(required=True),
    entry = fields.String(required=True)

class TaxonPath(Schema):
    source = fields.String(required=True)
    taxon = fields.Nested(Taxon)  # Must be many=True
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['taxon']) is dict:
    #        indata['taxon'] = [indata['taxon']] 

class Classification(Schema):
    purpose = fields.String(required=True)
    taxonPath = fields.Nested(TaxonPath)  # Must be many=True
    description = fields.String(required=True)
    keyword = fields.List(fields.String(), required=True)
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['taxonPath']) is dict:
    #        indata['taxonPath'] = [indata['taxonPath']] 

class LearningObjectMetadata(Schema):
    general = fields.Nested(General)
    lifecycle = fields.Nested(LifeCycle)
    metametadata = fields.Nested(MetaMetadata)
    technical = fields.Nested(Technical)
    educational = fields.Nested(Educational)
    rights = fields.Nested(Rights)
    relation = fields.Nested(Relation)
    annotation = fields.Nested(Annotation)
    classification = fields.Nested(Classification)
