
from flask_restful import request, Resource
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

client = Elasticsearch('193.112.33.124:9200')

class Query(Resource):
    def post(self):
        req = request.get_json()
        s = Search(using=client, index='hrent') \
            .filter('range', price={'gt': -1}) \
            .query('multi_match', query=req['title'], fields=['title', 'detail', 'address', 'traffic', 'house_type'])

        res = s.execute().to_dict()
        return res['hits']