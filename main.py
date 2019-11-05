import os

import mock
from flask import Flask, render_template, request
from google.cloud import datastore
import google.auth.credentials


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


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/test", methods=["GET"])
def test():
    return "NinjaTODO Test"


if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost", debug=True)  # localhost
