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
    # d = { 'xValue' : [],'yValue': []}
    # sampling = 10
    # print('in data function')
    # sampleSize = 1
    # while sampleSize < data_length:
    #     sampleSize *= 10
    #     sampling = sampleSize/10000
    #     print(sampling)
    # if sampling < 1:
    #     sampling = 1
    # # if(data_length > 100000):
    # #     sampling = 100
    # # if(data_length > 1000000):
    # #     sampling = 1000
    # i = 0
    # while i < data_length:
    #     if i % sampling == 0:
    #         d['xValue'].append(list_data['xValue'][i])
    #         d['yValue'].append(list_data['yValue'][i])
    #     i = i + 1
    # df2 = pd.DataFrame(data=d) 
    # chart_data = df2.to_dict(orient='records')
    # data = json.dumps(chart_data)
    data = create_dataset(data_length)

    return jsonify(data)

@app.route('/zoom_data')
def zoom_data():
    print('\nin zoom data function\n')
    # zoom_d = { 'xValue' : [],'yValue': []}
    # # new sample size with be the size of our length domain
    # sampleSize = x_max - x_min
    # if sampleSize > 100000:
    #     sample = 100
    # elif sampleSize > 1000000:
    #     sample = 1000
    # else:
    #     sample = 1
    # i = x_min
    # while i <= x_max:
    #     if(i % sample == 0):
    #         zoom_d['xValue'].append(list_data['xValue'][i])
    #         zoom_d['yValue'].append(list_data['yValue'][i])
    #     i = i + 1
    # create a new data set to create a chart 
    # from in index.js
    # df2 = pd.DataFrame(data = zoom_d)
    # chart_data = df2.to_dict(orient ='records')
    # data = json.dumps(chart_data)

    return jsonify(data)

def create_dataset(sampleSize):

    d = { 'xValue' : [],'yValue': []}

    if(sampleSize > 100000):
        sampling = 100
    elif (sampleSize > 1000000):
        sampling = 1000
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