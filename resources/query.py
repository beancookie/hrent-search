
from flask_restful import request, Resource
from elasticsearch_dsl import Search, MultiSearch
from elasticsearch import Elasticsearch

client = Elasticsearch('193.112.33.124:9200')

class Query(Resource):
    def post(self):
        params = request.get_json()['params']
        print(params)
        if 'url' in params:
            return Search(using=client, index='hrent').query('match', url=params['url']).execute().to_dict()
        
        search = Search(using=client, index='hrent') \
            .params(size=50) \
            .filter('range', price={'gt': 300}) \
            .filter('range', area={'gt': -1}) \
            .filter('term', _type='ziroom') \
            .filter('match', city=params['city']) \
            .query('multi_match', query=params['keyword'], fields=['title', 'address', 'traffic']) 

        if 'price' in params:
            if int(params['price']) != -1:
                search = search.filter('range', price={'gte': int(params['price']) - 1000, 'lte': int(params['price'])})
            else:
                search = search.filter('range', price={'gt': 300})
        if 'decorate' in params:
            search = search.query('match', decorate=params['decorate']) 
        
        if 'orientation' in params:
            search = search.query('term', orientation=params['orientation']) 
        res = search.execute().to_dict()
        return res['hits']