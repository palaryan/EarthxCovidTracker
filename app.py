import requests
import numpy as np
import time
import json
from rnn import train_and_predict, create_sample_data
from spotchain.Spotchain import Spotchain, Block
from flask import Flask, jsonify, request
from interface import Interface


app = Flask(__name__)
wrapper = Interface()
f = open("generate", "r")
matched_coords = eval(f.readline().strip("\n"))
s = Spotchain()
s.create_genesis_block()
"""
We don't have a live data set so we generate data for a specific coordinate for demoing purposes
"""
loc_history = json.dumps({"32.821002, -96.802862": create_sample_data(12).tolist()})

loc_block = Block(1, loc_history, time.time(), s.last_block.hash)
proof = loc_block.compute_hash()
loc = s.add_block(loc_block , proof)
@app.route('/nearby_users', methods=['GET'])
def ret_coords():
    if request.method == 'GET':
        print("GET")
        x = float(request.args.get("x"))
        y = float(request.args.get("y"))
        radius = float(request.args.get("radius"))
        
        #matched_coords = wrapper.grab_nearby_users(x, y, radius)
        '''
        Due to the fact that our team is unable to move around due to current restrictions, we used a set of generated test data that we loaded in our backend. Since this normally isn't 
        persistent data, it has not been integrated within our blockchain
        '''
        if matched_coords != "Not Found":
            return jsonify(matched_coords)
        else:
            return jsonify('empty')
    else:
        return jsonify("Wrong method") 


@app.route('/get_score', methods=['GET'])
def ret_score():
    if request.method == "GET":
        latbias = float(request.args.get("latbias"))
        longbias = float(request.args.get("longbias"))
        query = str(request.args.get("query"))
        query.replace(" ", "+")
        r = requests.get(f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery&fields=name,geometry&locationbias=point:{latbias},{longbias}&key=INSERTAPIKEY").json()
        title = r["candidates"][0]["name"]
        coords = r["candidates"][0]["geometry"]["location"]
        x1 = coords['lat']
        y1 = coords['lng']
        x2 = r["candidates"][0]["geometry"]["viewport"]["northeast"]["lat"]
        y2 = r["candidates"][0]["geometry"]["viewport"]["northeast"]["lng"] 
        x3 = r["candidates"][0]["geometry"]["viewport"]["southwest"]["lat"]
        y3 = r["candidates"][0]["geometry"]["viewport"]["southwest"]["lng"]
        corners = [(x2, y2), (x3, y3)]
        ret = wrapper.get_score(corners)
        return jsonify({"title":title, "coordinates":{"latitude":x1, "longitude":y1}, "score":ret})
    else:
        return jsonify("Wrong method")
@app.route('/time_travel', methods=['GET'])
def time_travel():
    if request.method == "GET":
        time.sleep(3)
        coord =  list(json.loads(s.chain[1].transactions).keys())[0]
        print(coord)
        x = float(request.args.get("x"))
        y = float(request.args.get("y"))
        radius = float(request.args.get("radius"))
        radius /= 4800
        radius /= 60
        hour = int(request.args.get("hours"))
        if ((x - float(coord.split(", ")[0])) ** 2 + (y - float(coord.split(", ")[1])) <= radius ** 2):
            return jsonify(train_and_predict(np.asarray(list(json.loads(s.chain[1].transactions).values())[0], dtype=np.float32), num_hours_looked_at=hour, show_results=False).tolist())

        else:
            return jsonify("Requested coordinate not in data set")

app.run(host='0.0.0.0', port='1337')

