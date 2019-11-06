import os

import mock
from flask import Flask, render_template, request
from google.cloud import datastore
import google.auth.credentials
from handlers import public


app = Flask(__name__)

if os.getenv('GAE_ENV', '').startswith('standard'):
    # production
    db = datastore.Client()
else:
    # localhost
    os.environ["DATASTORE_DATASET"] = "test"
    os.environ["DATASTORE_EMULATOR_HOST"] = "localhost:8001"
    os.environ["DATASTORE_EMULATOR_HOST_PATH"] = "localhost:8001/datastore"
    os.environ["DATASTORE_HOST"] = "http://localhost:8001"
    os.environ["DATASTORE_PROJECT_ID"] = "test"

    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    db = datastore.Client(project="test", credentials=credentials)

app.add_url_rule(rule="/", endpoint="public.index", view_func=public.index, methods=["GET"])
app.add_url_rule(rule="/login", endpoint="public.login", view_func=public.login, methods=["GET", "POST"])
app.add_url_rule(rule="/register", endpoint="public.register", view_func=public.register, methods=["GET", "POST"])

if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost", debug=True)  # localhost
