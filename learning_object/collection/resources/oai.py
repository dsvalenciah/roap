from yattag import Doc, indent
from datetime import datetime
from manager.get_many import get_many


class Oai(object):
    def __init__(self, db_client):
        self.db_client = db_client
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

        if not (req.params.get('verb') and self.verbs.get(req.params.get('verb'))):
            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')):
                with tag('responseDate'):
                    text(datetime.strftime(
                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                with tag('request'):
                    text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                with tag('error', code='badVerb'):
                    text('Illegal verb')
        elif req.params.get('verb') == 'Identify':
            if(len(req.params.keys()) > 1):
                with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')):
                    with tag('responseDate'):
                        text(datetime.strftime(
                            datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                    with tag('request'):
                        text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                    with tag('error', code='badArgument'):
                        text('The request\'s arguments are not valid or missing')
            else:
                with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')):
                    with tag('responseDate'):
                        text(datetime.strftime(
                            datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                    with tag('request', verb='Identify'):
                        text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                    with tag('Identify'):
                        with tag('repositoryName'):
                            text('ROAp')
                        with tag('baseURL'):
                            text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
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
            if not req.params.get('metadataPrefix'):
                with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')):
                    with tag('responseDate'):
                        text(datetime.strftime(
                            datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                    with tag('request'):
                        text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                    with tag('error', code='badArgument'):
                        text('The request\'s arguments are not valid or missing')
            elif not self.metadataPrefix.get(req.params.get('metadataPrefix')):
                with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')):
                    with tag('responseDate'):
                        text(datetime.strftime(
                            datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                    with tag('request'):
                        text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                    with tag('error', code='cannotDisseminateFormat'):
                        text(
                            f'{req.params.get("metadataPrefix")} is not supported by the item or by the repository')
            elif req.params.get('metadataPrefix') == 'lom':
                learning_objects, total_count = get_many(
                    db_client=self.db_client,
                    filter_={},
                    range_=[0, 9],
                    sorted_=["id", "DESC"],
                    user=req.context.get('user'),
                    learning_object_format='xml'
                )
                with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')):
                    with tag('responseDate'):
                        text(datetime.strftime(
                            datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                    with tag('request'):
                        text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                    with tag('ListRecords'):
                        for lo in learning_objects:
                            with tag('record'):
                                with tag('metadata'):
                                    text(lo.get('metadata'))

        resp.content_type = 'text/xml'
        result = indent(
            doc.getvalue(),
            indentation=' '*4,
            newline='\r\n'
        )
        resp.body = result
