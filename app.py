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
data_length = data = len(list_data['xValue'])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data')
def getData():
    # getting the fetched in data that is passed in when
    # the /data is called on the server side. 
    # x = request.args.get("x") # x range
    # y = request.args.get("y") # y range
    # k = request.args.get("k") # zoom level
    
    # calculate what points to return..
    data = create_dataset(data_length)

    return jsonify(data)

@app.route('/zoom_data')
def zoom_data():
    print('\nin zoom data function python\n')

    x_min = int(request.args.get('x_min'))
    x_max = int(request.args.get('x_max'))

    # create a new data set with more accurate data 
    data = create_dataset(x_max - x_min)

    return jsonify(data)


# creates data sets that will be used
# in the json for graphing
def create_dataset(sampleSize):

    d = { 'xValue' : [],'yValue': []}

    if(sampleSize > 1000000):
        sampling = 1000
    elif (sampleSize > 10000):
        sampling = 100
    elif (sampleSize > 1000):
        sampling = 10
    else :
        sampling = 1
    i = 0
    while i < sampleSize:
        if i % sampling == 0:
            d['xValue'].append(list_data['xValue'][i])
            d['yValue'].append(list_data['yValue'][i])
        i = i + 1
    df2 = pd.DataFrame(data=d) 
    chart_data = df2.to_dict(orient='records')
    data = json.dumps(chart_data)
    return data

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')