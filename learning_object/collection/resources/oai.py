from yattag import Doc, indent
from datetime import datetime
from manager.get_many import get_many
import jwt
import os


class Oai(object):
    def __init__(self, db_client):
        self.db_client = db_client
        self.valid_arguments = {
            'verb': True,
            'metadataPrefix': True,
            'resumptionToken': True
        }
        self.verbs = {
            'Identify': True,
            'ListRecords': True
        }
        self.metadataPrefix = {
            'lom': True
        }

    def on_get(self, req, resp):
        doc, tag, text = Doc().tagtext()
        req.context['user'] = {
            '_id': None,
            'role': 'external'
        }
        doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
        is_valid = True

        for key in req.params.keys():
            if(not self.valid_arguments.get(key)):
                is_valid = False
                break

        if not is_valid:
            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                with tag('responseDate'):
                    text(datetime.strftime(
                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                with tag('request'):
                    text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                with tag('error', code='badArgument'):
                    text('The request\'s arguments are not valid or missing')
        else:
            if not (req.params.get('verb') and self.verbs.get(req.params.get('verb')) and is_valid):
                with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                    with tag('responseDate'):
                        text(datetime.strftime(
                            datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                    with tag('request'):
                        text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                    with tag('error', code='badVerb'):
                        text('Illegal verb')
            elif req.params.get('verb') == 'Identify':
                if(len(req.params.keys()) > 1):
                    with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                        with tag('responseDate'):
                            text(datetime.strftime(
                                datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                        with tag('request', verb='Identify'):
                            text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                        with tag('error', code='badArgument'):
                            text('The request\'s arguments are not valid or missing')
                else:
                    with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                        with tag('responseDate'):
                            text(datetime.strftime(
                                datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                        with tag('request', verb='Identify'):
                            text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                        with tag('Identify'):
                            with tag('repositoryName'):
                                text('ROAp')
                            with tag('baseURL'):
                                text(
                                    'http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
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
                            text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                        with tag('error', code='badArgument'):
                            text('The request\'s arguments are not valid or missing')
                elif req.params.get('metadataPrefix') == 'lom' or req.params.get('resumptionToken'):
                    if(req.params.get('resumptionToken')):
                        try:
                            resumptionToken = jwt.decode(
                                req.params.get('resumptionToken'),
                                os.getenv('JWT_SECRET'),
                                verify='True',
                                algorithms=['HS512']
                            )

                            learning_objects, total_count = get_many(
                                db_client=self.db_client,
                                filter_={},
                                range_=[int(resumptionToken.get('cursor')), int(
                                    resumptionToken.get('cursor')) + 1],
                                sorted_=["id", "DESC"],
                                user=req.context.get('user'),
                                learning_object_format='xml'
                            )

                            token = jwt.encode({
                                'cursor': int(
                                    resumptionToken.get('cursor')) + 1
                            },
                                os.getenv('JWT_SECRET'),
                                algorithm='HS512').decode('utf-8')
                            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                                with tag('responseDate'):
                                    text(datetime.strftime(
                                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                                with tag('request', verb="ListRecords", resumptionToken=req.params.get('resumptionToken')):
                                    text(
                                        'http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
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
                                        'http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                                with tag('error', code='badResumptionToken'):
                                    text(
                                        'The value of the resumptionToken argument is invalid or expired')
                    else:
                        learning_objects, total_count = get_many(
                            db_client=self.db_client,
                            filter_={},
                            range_=[0, 1],
                            sorted_=["id", "DESC"],
                            user=req.context.get('user'),
                            learning_object_format='xml'
                        )
                        token = jwt.encode({
                            'cursor': 2
                        },
                            os.getenv('JWT_SECRET'),
                            algorithm='HS512').decode('utf-8')
                        with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                            with tag('responseDate'):
                                text(datetime.strftime(
                                    datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                            with tag('request', verb='ListRecords', metadataPrefix='lom'):
                                text(
                                    'http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
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
                elif not self.metadataPrefix.get(req.params.get('metadataPrefix')):
                    with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'), ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')):
                        with tag('responseDate'):
                            text(datetime.strftime(
                                datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                        with tag('request'):
                            text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
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
