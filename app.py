import json
from flask import Flask, render_template,jsonify,url_for, Response,request,redirect
import pandas as pd
import math

app = Flask(__name__)

# open the file
df = pd.read_csv('data/tenthousand.csv')
# chart_data = df.to_dict(orient='records')
list_data = df.to_dict(orient='list')
min = 0
# must do the len of the xValue because there is only
# two attributes so inorder to get the number of indexes you
# need to len of the one of the attributes
max = len(list_data['xValue'])
data_length = data = len(list_data['xValue'])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data')
def getData():
    # This is the initial time we make the graph. Our xMin will
    # alway be the first index in x Value of the data. Our xMax
    # will be the last index in x Value of the data. 
    data = create_dataset(data_length, list_data['xValue'][0], list_data['xValue'][data_length - 1])
    return jsonify(data)

@app.route('/zoom_data')
def zoom_data():
    # getting the fetched in data that is passed in when
    # the /zoom_data is called on the server side. 
    x_min = int(request.args.get('x_min')) # x min of range
    x_max = math.ceil(float(request.args.get('x_max'))) # x max of range
    zoom_level = float(request.args.get('zoom_level')) 

    # off by one error so add 1
    Xrange = x_max - x_min + 1

    if x_max == data_length:
        x_max = x_max - 1
    data = create_dataset(Xrange, x_min, x_max)
    return jsonify(data)


# creates data sets that will be used
# in the json for graphing
def create_dataset(sampleSize,x_min,x_max):

    d = { 'xValue' : [],'yValue': []}

    if(sampleSize > 1000000):
        sampling = 10000
    elif (sampleSize > 100000):
        sampling = 1000
    elif (sampleSize > 10000):
        sampling = 100
    elif (sampleSize > 1000):
        sampling = 10
    else:
        sampling = 1
    i = 0
    j = x_min
    while i < sampleSize:
        if i % sampling == 0:
            if j >= list_data['xValue'][x_min] and j <= list_data['xValue'][x_max]:
                d['xValue'].append(list_data['xValue'][j])
                d['yValue'].append(list_data['yValue'][j])
        i = i + 1
        j = j + 1

    df2 = pd.DataFrame(data=d) 
    chart_data = df2.to_dict(orient='records')
    data = json.dumps(chart_data)
    return data

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')