import json
from flask import Flask, render_template,jsonify,url_for, Response,request,redirect
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('timeData.csv')
chart_data = df.to_dict(orient='records')
data = json.dumps(chart_data)

@app.route('/')
def index():
    return render_template("index.html", data=data)

@app.route('/data')
def getData():
    # getting the fetched in data that is passed in when
    # the /data is called on the server side. 
    # x = request.args.get("x") # x range
    # y = request.args.get("y") # y range
    # k = request.args.get("k") # zoom level
    
    # calculate what points to return...

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')