
from flask_restful import request, Resource
from elasticsearch_dsl import Search, MultiSearch
from elasticsearch import Elasticsearch

client = Elasticsearch('193.112.33.124:9200')

class Query(Resource):
    def post(self):
        params = request.get_json()['params']
        
        search = Search(using=client, index='hrent') \
            .filter('range', price={'gt': 300}) \
            .query('multi_match', query=params['keyword'], fields=['title', 'detail', 'address', 'traffic', 'house_type'])
        
        if 'price' in params:
            if int(params['price']) != -1:
                search = search.filter('range', price={'gte': int(params['price']) - 1000, 'lte': int(params['price'])})
            else:
                search = search.filter('range', price={'gt': 300})
        if 'decorate' in params:
            search = search.query('match', decorate=params['decorate']) 
        
        if 'rent_type' in params:
            search = search.query('match', rent_type=params['rent_type']) 
        res = search.execute().to_dict()
        return res['hits']