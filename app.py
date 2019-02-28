import json
from flask import Flask, render_template,jsonify,url_for, Response,request,redirect
import pandas as pd

app = Flask(__name__)

# open the file
df = pd.read_csv('data/million.csv')
# chart_data = df.to_dict(orient='records')
list_data = df.to_dict(orient='list')
min = 0
# must do the len of the xValue because there is only
# two attributes so inorder to get the number of indexs you
# need to len of the one of the attributes
max = len(list_data['xValue'])
# data = json.dumps(chart_data)

d = { 'xValue' : [],'yValue': []}
# df2 = pd.DataFrame(data=d)
# newchart = df2.to_dict(orient='records')
# data = json.dumps(newchart)
# data = 0
# print(newchart)
sampling = 10

sampleSize=1
while sampleSize < (max-min):
    sampleSize *= 10
sampling = sampleSize/1000
if sampling < 1:
    sampling = 1
i = 0
while i < max:
    if i % sampling == 0:
        d['xValue'].append(list_data['xValue'][i])
        d['yValue'].append(list_data['yValue'][i])
    i = i + 1
df2 = pd.DataFrame(data=d) 
chart_data = df2.to_dict(orient='records')
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