import flask
import logging
from flask_restful import Api
from resources.rules import Rules


def create_app():
    return flask.Flask('api')

logging.getLogger().setLevel(logging.INFO)

app = create_app()
api = Api(app)
api.add_resource(Rules, '/api/rules')

if __name__ == '__main__':
    app.run(debug=True)
