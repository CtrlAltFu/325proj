# -*- coding: utf-8 -*-
"""

@author: mpawel
"""

from flask import Flask, request
# TO generate UI for sending request via browser
from flasgger import Swagger
import json
import urllib.request
import ssl
import os

app = Flask(__name__)

# Enable this app for swagger and it will auto generate UI
swagger = Swagger(app)

scoring_uri = 'http://6dedce89-03cb-4eec-9809-cf915d6e00c4.eastus.azurecontainer.io/score'


# Set the content type
headers = {'Content-Type':'application/json'}


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)


@app.route('/btcPredict', methods=['POST'])
def predict_price():
    # BELOW docstring lines are required to support swagger documentation
    """ Endpoint returning titanic survival prediction
    ---
    parameters:
        - name: todayprice
          in: formData
          type: string
          required: true
    """
    todayprice = request.form["todayprice"]

    todayprice = float(todayprice)

    todayprice = {"data": [todayprice]}

    todayprice = str.encode(json.dumps(todayprice))

    req = urllib.request.Request(scoring_uri, todayprice, headers)


    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))


    # Send the prediction as response - will need to convert number to string
    return str(result)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
