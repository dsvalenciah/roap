
"""
Contains utility functions to works with learning-object and his metadata
fields schemas.
"""

from marshmallowjson.marshmallowjson import Definition

def LearningObjectMetadata(db_client):
    """Check if learning-object matches with a learning-object schema."""
    lom_schema = list(
        db_client.lom_schema.find().sort("created", -1).limit(1)
    )[0].get('lom')
    return Definition(lom_schema).top()

"""
# TODO: to add many nested fields, add many=False in all nested fields
# handle it with @predump and add the multiple forms in the front end
from marshmallow import Schema, fields, validate, pre_dump

class Identifier(Schema):
    catalog = fields.String(required=False, allow_none=True)
    entry = fields.String(required=False, allow_none=True)

class General(Schema):
    identifier = fields.Nested(Identifier)  # Must be many=False
    title = fields.String(required=True)
    language = fields.List(fields.String(), required=False, allow_none=True)
    description = fields.List(fields.String(), required=True)
    keyword = fields.List(fields.String(), required=False, allow_none=True)
    coverage = fields.List(fields.String(), required=False, allow_none=True)
    structure = fields.String(required=False, allow_none=True)
    aggregationlevel = fields.String(
        required=False,
        allow_none=True
    )
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['identifier']) is dict:
    #        indata['identifier'] = [indata['identifier']] 

class Contribute(Schema):
    role = fields.String(required=False, allow_none=True)
    date = fields.DateTime(required=False, allow_none=True)
    entity = fields.List(fields.String(), required=False, allow_none=True)

class LifeCycle(Schema):
    version = fields.String(required=False, allow_none=True)
    status = fields.String(required=False, allow_none=True)
    contribute = fields.List(fields.String(), required=False, allow_none=True)

class MetaMetadata(Schema):
    identifier = fields.Nested(Identifier)  # Must be many=False
    contribute = fields.Nested(Contribute)  # Must be many=False
    metadataschema = fields.String(required=False, allow_none=True)
    language = fields.List(fields.String(), required=False, allow_none=True)
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['identifier']) is dict:
    #        indata['identifier'] = [indata['identifier']]
    #    if type(indata['contribute']) is dict:
    #        indata['contribute'] = [indata['contribute']]

class Orcomposite(Schema):
    type = fields.String(required=False, allow_none=True)
    name = fields.String(required=False, allow_none=True)
    minimumversion = fields.String(required=False, allow_none=True)
    maximumversion = fields.String(required=False, allow_none=True)

class Requirements(Schema):
    orcomposite = fields.Nested(Orcomposite)  # Must be many=False
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['orcomposite']) is dict:
    #        indata['orcomposite'] = [indata['orcomposite']] 

class Technical(Schema):
    format = fields.List(fields.String(), required=False, allow_none=True)
    size =  fields.String(required=False, allow_none=True)
    location = fields.List(fields.String(), required=False, allow_none=True)
    requirements = fields.Nested(Requirements)  # Must be many=False
    installationremarks = fields.List(fields.String(), required=False, allow_none=True)
    otherplatformrequirements = fields.List(fields.String(), required=False, allow_none=True)
    duration =  fields.String(required=False, allow_none=True)
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['requirements']) is dict:
    #        indata['requirements'] = [indata['requirements']] 

class Educational(Schema):
    interactivitytype = fields.String(required=False, allow_none=True)
    learningresourcetype = fields.List(fields.String(), required=False, allow_none=True)
    interactivitylevel = fields.String(
        required=False,
        allow_none=True)
    )
    semanticdensity = fields.String(
        required=False,
        allow_none=True
    )
    intendedenduserrole = fields.List(fields.String(), required=False, allow_none=True)
    context = fields.List(fields.String(), required=False, allow_none=True)
    typicalagerange = fields.List(fields.String(), required=False, allow_none=True)
    difficulty = fields.String(
        required=False,
        allow_none=True
    )
    typicallearningtime = fields.String(required=False, allow_none=True)
    description = fields.List(fields.String(), required=False, allow_none=True)
    language = fields.List(fields.String(), required=False, allow_none=True)

class Rights(Schema):
    cost = fields.String(required=False, allow_none=True)
    copyrightandotherrestrictions = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)

class Resource(Schema):
    identifier = fields.Nested(Identifier)  # Must be many=False
    description = fields.List(fields.String(), required=False, allow_none=True)
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['identifier']) is dict:
    #        indata['identifier'] = [indata['identifier']] 

class Relation(Schema):
    kind = fields.String(required=False, allow_none=True)
    resource = fields.Nested(Resource)  # Must be many=False
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['resource']) is dict:
    #        indata['resource'] = [indata['resource']] 

class Annotation(Schema):
    entity = fields.String(required=False, allow_none=True)
    date = fields.DateTime(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)

class Taxon(Schema):
    id = fields.String(required=False, allow_none=True)
    entry = fields.String(required=False, allow_none=True)

class TaxonPath(Schema):
    source = fields.String(required=False, allow_none=True)
    taxon = fields.Nested(Taxon)  # Must be many=False
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['taxon']) is dict:
    #        indata['taxon'] = [indata['taxon']] 

class Classification(Schema):
    purpose = fields.String(required=False, allow_none=True)
    taxonPath = fields.Nested(TaxonPath)  # Must be many=False
    description = fields.String(required=False, allow_none=True)
    keyword = fields.List(fields.String(), required=False, allow_none=True)
    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['taxonPath']) is dict:
    #        indata['taxonPath'] = [indata['taxonPath']] 

class PresentationMode(Schema):
    auditory = fields.String(required=False, allow_none=True)
    textual = fields.String(required=False, allow_none=True)
    visual = fields.String(required=False, allow_none=True)

class InteractionMode(Schema):
    keyboard = fields.String(required=False, allow_none=True)
    mouse = fields.String(required=False, allow_none=True)
    voicerecognition = fields.String(required=False, allow_none=True)

class AdaptationType(Schema):
    audiodescription = fields.String(required=False, allow_none=True)
    hearingalternative = fields.String(required=False, allow_none=True)
    signlanguage= fields.String(required=False, allow_none=True)
    subtitles = fields.String(required=False, allow_none=True)

class Accessibility(Schema):
    presentationmode = fields.Nested(PresentationMode)
    interactionmode = fields.Nested(InteractionMode)
    adaptationtype = fields.Nested(AdaptationType)

    #@pre_dump
    #def wrap_indata(self, indata):
    #    if type(indata['presentationmode']) is dict:
    #        indata['presentationmode'] = [indata['presentationmode']]
    #    if type(indata['interactionmode']) is dict:
    #        indata['interactionmode'] = [indata['interactionmode']]
    #    if type(indata['adaptationtype']) is dict:
    #        indata['adaptationtype'] = [indata['adaptationtype']]

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
    accessibility = fields.Nested(Accessibility)
"""
