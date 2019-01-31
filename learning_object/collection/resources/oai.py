from yattag import Doc, indent
from datetime import datetime
from manager.get_many import get_many
import jwt
import os


class Oai(object):
    def __init__(self, db_client):
        self.db_client = db_client
        self.valid_arguments = [
            'verb',
            'metadataPrefix',
            'resumptionToken',
            'from',
            'until',
            'set'
        ]
        self.valid_verbs = [
            'Identify',
            'ListRecords'
        ]
        self.valid_metadata_prefix = [
            'lom'
        ]

    def on_get(self, req, resp):
        doc, tag, text = Doc().tagtext()
        filters = {}
        req.context['user'] = {
            '_id': None,
            'role': 'external'
        }
        doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
        is_valid = True

        for key in req.params.keys():
            if(not key in self.valid_arguments):
                is_valid = False
                break

        if not is_valid:
            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                with tag('responseDate'):
                    text(datetime.strftime(
                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                with tag('request'):
                    text('http://gaia.manizales.unal.edu.co:8081/v1/oai')
                with tag('error', code='badArgument'):
                    text('The request\'s arguments are not valid or missing')
        else:
            if not (req.params.get('verb') and req.params.get('verb') in self.valid_verbs):
                with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                    with tag('responseDate'):
                        text(datetime.strftime(
                            datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                    with tag('request'):
                        text('http://gaia.manizales.unal.edu.co:8081/v1/oai')
                    with tag('error', code='badVerb'):
                        text('Illegal verb')
            elif req.params.get('verb') == 'Identify':
                if(len(req.params.keys()) > 1):
                    with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                        with tag('responseDate'):
                            text(datetime.strftime(
                                datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                        with tag('request', verb='Identify'):
                            text('http://gaia.manizales.unal.edu.co:8081/v1/oai')
                        with tag('error', code='badArgument'):
                            text('The request\'s arguments are not valid or missing')
                else:
                    with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                        with tag('responseDate'):
                            text(datetime.strftime(
                                datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                        with tag('request', verb='Identify'):
                            text('http://gaia.manizales.unal.edu.co:8081/v1/oai')
                        with tag('Identify'):
                            with tag('repositoryName'):
                                text('ROAp')
                            with tag('baseURL'):
                                text(
                                    'http://gaia.manizales.unal.edu.co:8081/v1/oai')
                            with tag('protocolVersion'):
                                text('2.0')
                            with tag('adminEmail'):
                                text('roap@unal.edu.co')
                            with tag('deleteRecord'):
                                text('transient')
                            with tag('granularity'):
                                text('YYYY-MM-DDThh:mm:ssZ')
                            with tag('compression'):
                                text('deflate')

            elif req.params.get('verb') == 'ListRecords':
                if not req.params.get('metadataPrefix') and not req.params.get('resumptionToken') or (req.params.get('metadataPrefix') and req.params.get('resumptionToken')):
                    with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                        with tag('responseDate'):
                            text(datetime.strftime(
                                datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                        with tag('request'):
                            text('http://gaia.manizales.unal.edu.co:8081/v1/oai')
                        with tag('error', code='badArgument'):
                            text('The request\'s arguments are not valid or missing')
                elif req.params.get('set'):
                    with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                        with tag('responseDate'):
                            text(datetime.strftime(
                                datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                        with tag('request'):
                            text('http://gaia.manizales.unal.edu.co:8081/v1/oai')
                        with tag('error', code='noSetHierarchy'):
                            text('The repository does not support sets')
                elif req.params.get('metadataPrefix') == 'lom' or req.params.get('resumptionToken'):
                    if(req.params.get('resumptionToken')):
                        if(req.params.get('from') or req.params.get('until')):
                            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                                with tag('responseDate'):
                                    text(datetime.strftime(
                                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                                with tag('request'):
                                    text(
                                        'http://gaia.manizales.unal.edu.co:8081/v1/oai')
                                with tag('error', code='badArgument'):
                                    text(
                                        'The request\'s arguments are not valid or missing')
                        try:
                            resumptionToken = jwt.decode(
                                req.params.get('resumptionToken'),
                                os.getenv('JWT_SECRET'),
                                verify='True',
                                algorithms=['HS512']
                            )

                            if(resumptionToken.get('from')):
                                filters['modified'] = {
                                    '$gte': resumptionToken.get('from') + ' 00:00:00'}

                            if(resumptionToken.get('until')):
                                if(filters.get('modified')):
                                    filters['modified'].update(
                                        {'$lte': resumptionToken.get('until') + ' 23:59:59'})
                                else:
                                    filters['modified'] = {
                                        '$lte': resumptionToken.get('until')}

                            learning_objects, total_count = get_many(
                                db_client=self.db_client,
                                filter_=filters,
                                range_=[int(resumptionToken.get('cursor')), int(
                                    resumptionToken.get('cursor')) + int(os.getenv('LOS_PER_PAGE_OAI_PMH')) - 1],
                                sorted_=["id", "DESC"],
                                user=req.context.get('user'),
                                learning_object_format='xml'
                            )
                            token_info = {
                                'cursor': int(
                                    resumptionToken.get('cursor')) + int(os.getenv('LOS_PER_PAGE_OAI_PMH'))
                            }

                            if(resumptionToken.get('from')):
                                token_info['from'] = req.params.get('from')

                            if(resumptionToken.get('until')):
                                token_info['until'] = req.params.get('until')

                            token = jwt.encode(token_info,
                                               os.getenv('JWT_SECRET'),
                                               algorithm='HS512').decode('utf-8')

                            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                                with tag('responseDate'):
                                    text(datetime.strftime(
                                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                                with tag('request', verb="ListRecords", resumptionToken=req.params.get('resumptionToken')):
                                    text(
                                        'http://gaia.manizales.unal.edu.co:8081/v1/oai')
                                with tag('ListRecords'):
                                    for lo in learning_objects:
                                        with tag('record'):
                                            with tag('header'):
                                                with tag('identifier'):
                                                    text(lo.get('_id'))
                                                with tag('modified'):
                                                    text(lo.get('modified'))
                                            with tag('metadata'):
                                                doc.asis(lo.get('metadata'))
                                    if(len(learning_objects) + int(resumptionToken.get('cursor')) < total_count):
                                        with tag('resumptionToken', cursor=resumptionToken.get('cursor')):
                                            text(token)

                        except:
                            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                                with tag('responseDate'):
                                    text(datetime.strftime(
                                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                                with tag('request'):
                                    text(
                                        'http://gaia.manizales.unal.edu.co:8081/v1/oai')
                                with tag('error', code='badResumptionToken'):
                                    text(
                                        'The value of the resumptionToken argument is invalid or expired')
                    else:
                        if(req.params.get('from')):
                            filters['modified'] = {
                                '$gte': req.params.get('from') + ' 00:00:00'}

                        if(req.params.get('until')):
                            if(filters.get('modified')):
                                filters['modified'].update(
                                    {'$lte': req.params.get('until') + ' 23:59:59'})
                            else:
                                filters['modified'] = {
                                    '$lte': req.params.get('until')}

                        learning_objects, total_count = get_many(
                            db_client=self.db_client,
                            filter_=filters,
                            range_=[0, int(os.getenv('LOS_PER_PAGE_OAI_PMH')) - 1],
                            sorted_=["id", "DESC"],
                            user=req.context.get('user'),
                            learning_object_format='xml'
                        )

                        token_info = {
                            'cursor': int(os.getenv('LOS_PER_PAGE_OAI_PMH'))
                        }

                        if(req.params.get('from')):
                            token_info['from'] = req.params.get('from')

                        if(req.params.get('until')):
                            token_info['until'] = req.params.get('until')

                        if(len(learning_objects)):
                            token = jwt.encode(token_info,
                                               os.getenv('JWT_SECRET'),
                                               algorithm='HS512').decode('utf-8')

                            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                                with tag('responseDate'):
                                    text(datetime.strftime(
                                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                                with tag('request', verb='ListRecords', metadataPrefix='lom'):
                                    if req.params.get('from'):
                                        doc.attr(
                                            ('from', req.params.get('from')))

                                    if req.params.get('until'):
                                        doc.attr(until=req.params.get('until'))
                                    text(
                                        'http://gaia.manizales.unal.edu.co:8081/v1/oai')
                                with tag('ListRecords'):
                                    for lo in learning_objects:
                                        with tag('record'):
                                            with tag('header'):
                                                with tag('identifier'):
                                                    text(lo.get('_id'))
                                                with tag('modified'):
                                                    text(lo.get('modified'))
                                            with tag('metadata'):
                                                doc.asis(lo.get('metadata'))
                                    if(len(learning_objects) < total_count):
                                        with tag('resumptionToken', cursor=0):
                                            text(token)
                        else:
                            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                                with tag('responseDate'):
                                    text(datetime.strftime(
                                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                                with tag('request'):
                                    text(
                                        'http://gaia.manizales.unal.edu.co:8081/v1/oai')
                                with tag('error', code='noRecordsMatch'):
                                    text(
                                        'The combination of the values of the from, until, set and metadataPrefix arguments results in an empty list.')
                elif not req.params.get('metadaPrefix') in self.valid_metadata_prefix:
                    with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                        with tag('responseDate'):
                            text(datetime.strftime(
                                datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                        with tag('request'):
                            text('http://gaia.manizales.unal.edu.co:8081/v1/oai')
                        with tag('error', code='cannotDisseminateFormat'):
                            text(
                                f'{req.params.get("metadataPrefix")} is not supported by the item or by the repository')

        resp.content_type = 'text/xml'
        result = indent(
            doc.getvalue(),
            indentation=' '*4,
            newline='\r\n'
        )
        resp.body = result
