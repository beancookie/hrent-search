
from flask_restful import request, Resource
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

client = Elasticsearch('193.112.33.124:9200')

class Query(Resource):
    def get(self):
        req = request.get_json()
        s = Search(using=client, index='hrent') \
            .query('match', title=req['title'])

        res = s.execute().to_dict()
        return res['hits']