from flask import Flask
from flask import request, jsonify
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
app = Flask(__name__)
client = Elasticsearch('193.112.33.124:9200')

@app.route('/search')
def search():
    query = request.get_json()
    print(query)
    s = Search(using=client, index="hrent") \
        .query("match", title=query['title'])

    response = s.execute()
    return jsonify(response.to_dict()['hits'])


if __name__ == '__main__':
    app.run()
