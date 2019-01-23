from yattag import Doc, indent
from datetime import datetime


class Oai(object):
    def __init__(self, db_client):
        self.db_client = db_client
        self.verbs = {
            'Identify': True,
            'ListRecords': True
        }

    def on_get(self, req, resp):
        if not req.params.get('verb') or not self.verbs.get(req.params.get('verb')):
            resp.content_type = 'text/xml'
            doc, tag, text = Doc().tagtext()
            with tag('OAI-PMH',  ('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')):
                with tag('responseDate'):
                    text(datetime.strftime(
                        datetime.now(), format="%Y-%m-%d %H:%M:%S"))
                with tag('request'):
                    text('http://gaia.manizales.unal.edu.co/roapRAIM/oai.php')
                with tag('error', code='badVerb'):
                    text('Illegal verb')

            result = indent(
                doc.getvalue(),
                indentation=' '*4,
                newline='\r\n'
            )
            resp.body = result
        elif req.params.get('verb') == 'Identify':
            resp.content_type = 'text/xml'
            doc, tag, text = Doc().tagtext()
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

            result = indent(
                doc.getvalue(),
                indentation=' '*4,
                newline='\r\n'
            )
            resp.body = result
