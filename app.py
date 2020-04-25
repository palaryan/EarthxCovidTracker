from flask import Flask, jsonify, request
from interface import Interface
app = Flask(__name__)
wrapper = Interface()
@app.route('/', methods=['POST'])
def response():
    if request.method == 'POST':
        x = float(request.args.get("x"))
        y = float(request.args.get("y"))
        radius = float(request.args.get("radius"))
        matched_coords = wrapper.grab_nearby_users(x, y, radius)
        if matched_coords != "Not Found":
            return jsonify({'matched_coords':matched_coords[0],'percentage': matched_coords[1]})
        else:
            return jsonify({'matched_coords':'empty'})
app.run(host='0.0.0.0', port='1337')

