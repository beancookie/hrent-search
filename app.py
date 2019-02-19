
from flask import Flask
from flask_restful import request, abort, Api, Resource
from resources.query import Query

app = Flask(__name__)
api = Api(app)


##
## Actually setup the Api resource routing here
##
api.add_resource(Query, '/query')


if __name__ == '__main__':
    app.run(debug=True)
