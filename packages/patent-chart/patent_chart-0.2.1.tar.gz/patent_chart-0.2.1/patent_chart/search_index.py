from elasticsearch import Elasticsearch

from . import settings
from . import parser

client = Elasticsearch(settings.ELASTIC_HOST)

def get_patent_summary(patent: parser.GoogleParsedPatent) -> str:
    response = client.get(index='patents', id=str(patent.unique_id))
    return response['_source'].get('summary')

def update_patent_by_id(patent: parser.GoogleParsedPatent, **kwargs):
    client.update(index='patents', id=str(patent.unique_id), body={'doc': kwargs})