import os
import requests

from flask import Flask


def create_app():
    # instantiate flask app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import blueprint ("controller")
    # sample exists at the same level as __init__ - . allows us to import files at the same level
    from . import sample

    # registers all blueprint routes to app
    app.register_blueprint(sample.bp)
    # app now has access to all routes defined within sample.py
    # app.add_url_rule('/', endpoint='index')

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # test methods for API calls
    @app.route('/apiTest')
    def api_test():
        api_result = requests.get('https://api.dccresource.com/api/games/5faac562db090e1a5c2dea0a')
        return api_result.content

    @app.route('/apiTest2')
    def api_test_2():
        api_result = requests.get('https://api.dccresource.com/api/games/5faac562db090e1a5c2dea0a')
        game = api_result.json()
        return 'Name: ' + game['name']

    return app
