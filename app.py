#!/usr/bin/env python

import urllib
import json
import os
import random

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    #if req.get("result").get("action") != "shipping.cost":
    if req.get("result").get("action") != "tell-status":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    #zone = parameters.get("shipping-zone")
    pnrnum = parameters.get("pnr")

    ran_a = randrange(1, 4)
    ran_b = randrange(1, 200)
    cost = uniform(1, 30)
    status = {'WL', 'RAC', 'Reserved'}


    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    speech = "The status of " + pnrnum + " is " + status[ran_a] + " " + str(ran_b) + ". Upgradation charges are " + str(cost) + "."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "agent4007"
        "followupEvent": {
            "name": "charge",
            "data": {
                "charges":"cost"
            }
        }
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
