import json
from flask import Flask, render_template,jsonify,url_for, Response,request,redirect
import pandas as pd
import math

app = Flask(__name__)

# open the file
df = pd.read_csv('data/ten.csv')
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
    data = create_dataset(data_length - 1, list_data['xValue'][0], list_data['xValue'][data_length - 1])
    return jsonify(data)

@app.route('/zoom_data')
def zoom_data():
    # getting the fetched in data that is passed in when
    # the /zoom_data is called on the server side. 
    x_min = int(request.args.get('x_min')) # x min of range
    x_max = math.ceil(float(request.args.get('x_max'))) # x max of range
    zoom_level = float(request.args.get('zoom_level')) 

    # off by one error so add 1 unless x range is our data length.
    Xrange = x_max - x_min + 1
    # preventing trying to access index bigger than or equal to our data length 
    if Xrange >= data_length:
        Xrange = data_length - 1

    if x_max >= data_length:
        x_max = x_max - 1
    data = create_dataset(Xrange, x_min, x_max)
    return jsonify(data)


# creates data sets that will be used
# in the json for graphing
def create_dataset(sampleSize,x_min,x_max):

    threshold = 1
    if sampleSize > 999999:
        threshold = 10000
    elif sampleSize > 99999:
        threshold = 1000
    elif sampleSize > 9999:
        threshold = 100
    elif sampleSize > 999:
        threshold = 10
    else:
        threshold
    print('List type' ,type(list_data))
    d = largest_triangle_three_bucket(list_data,threshold)
    if isinstance(d, str):
        return False
    df2 = pd.DataFrame(data = d)
    chart_data = df2.to_dict(orient='records')
    data = json.dumps(chart_data)
  
    return data


# class LttbException(Exception):
#     pass

def largest_triangle_three_bucket(data,threshold):
    # Check if data and threshold are valid
    if not isinstance(data,list):
        return print("data is not a list")
    if not isinstance(threshold, int) or threshold <= 2 or threshold >= len(data):
        return print("threshold not well defined")
    for i in data:
        if not isinstance(i, (list,tuple)) or len(i) != 2:
            return print("data points are not lists or tuples")

    # Bucket size. Leave room for start and end data points
    # because first and last bucket will only contant the first and last
    # data points
    every = (len(data) - 2) / (threshold - 2)

    a = 0 # letting a be the first point in the triangle
    next_a = 0
    max_area_point = (0,0)

    sampled = [data[0]] # adding the first point. this will always be done

    for i in range(0, threshold - 2):
        # calculating point average for next bucket (containing c)
        avg_x = 0
        avg_y = 0
        avg_range_start = int(math.floor((i + 1) * every) + 1)
        avg_range_end = int(math.floor((i + 1) * every) + 1)
        avg_rang_end = avg_range_end if avg_range_end < len(data) else len(data)

        avg_range_length = avg_rang_end - avg_range_start

        while avg_range_start < avg_rang_end:
            avg_x += data[avg_range_start][0]
            avg_y += data[avg_range_start][1]
            avg_range_start += 1
        
        avg_x /= avg_range_length
        avg_y /= avg_range_length

        # get range for this bucket
        range_offs = int(math.floor((i + 0) * every) + 1)
        range_to = int(math.floor((i + 0) * every) + 1)

        # point a
        point_ax = data[a][0]
        point_ay = data[a][1]

        while range_offs < range_to:
            # calculating triangle area over three buckets
            area = math.fabs(
                (point_ax - avg_x) * (data[range_offs][0])
                - (point_ax - data[range_offs][0])
                * (avg_y - point_ay)
            ) * 0.5

            if area > max_area:
                max_area = area
                max_area_point = data[range_offs]
                next_a = range_offs # next a is this b
            range_offs += 1

        sampled.append(max_area_point) # pick this point from the bucket
        a = next_a # this a is the next a (chosen b)

    # always add the last element of the data
    sampled.append(data[len(data) - 1]) 
    print('SAMPLED DATA: \n',sampled)

    return sampled

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')