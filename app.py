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
    if req.get("result").get("action") != "add-sum":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    #zone = parameters.get("shipping-zone")
    #pnrnum = parameters.get("pnr")
    
    tickets = float(parameters.get("tickets"))
    pcharges = float(parameters.get("ppcharges"))
    rcharges = float(parameters.get("rcharges"))
    mcharges = float(parameters.get("mcharges"))
    sumTotal = (tickets*mcharges) + pcharges + rcharges

    #ran_a = random.randrange(1, 4)
    #ran_b = random.randrange(1, 200)
    #cost = random.uniform(1, 30)
    #status = ["WL", "RAC", "Reserved"]


    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    #speech = "The status of " + str(pnrnum) + " is " + status[ran_a-1] + " " + str(ran_b) + ". Upgradation charges are USD " + str(cost) + "."
    speech = "Total amount to be paid is " + str(sumTotal) + ". This amount will be adjusted in your mobile bill for this month. Goodbye."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "hda007",
        "followupEvent": {
            #"name": "webcheck",
            "name": "finalSum",
            "data": {
                "sumTotal":str(sumTotal)
            }
        }
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
