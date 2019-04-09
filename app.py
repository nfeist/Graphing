import json
from flask import Flask, render_template,jsonify,url_for, Response,request,redirect
import pandas as pd
import math

app = Flask(__name__)

# open the file
df = pd.read_csv('data/hundredthousand.csv')
dict_data = df.to_dict(orient='split')
# must do the len of the xValue because there is only
# two attributes so inorder to get the number of indexes you
# need to len of the one of the attributes
data_length = data = len(dict_data['data'])
all_data = list(dict_data['data'])


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data')
def getData():
    # This is the initial time we make the graph
    data = create_dataset(all_data,480,960)
    return jsonify(data)

@app.route('/zoom_data')
def zoom_data():
    # getting the fetched in data that is passed in when
    # the /zoom_data is called on the server side. 
    zoom_level = float(request.args.get('zoom_level')) 
    width = int(request.args.get('width'))
    x_min = int(request.args.get('x_min'))
    x_max = int(request.args.get('x_max'))
    # we want to down sample more detail of a subset of all data
    subset_data = all_data[x_min : (x_max + 1)]

    data = create_dataset(subset_data, 480, 960)

    # rtn = { 
    #     "lttb": lttb_data,
    #     "min_max": min_max_data, 
    # }

    # return jsonify(rtn)

    return jsonify(data)


# creates data sets that will be used
# in the json for graphing
def create_dataset(data,threshold,width):
    # threshold = int((width / 12) * zoom_level)
    # print('new threshold: ',threshold)
    
    # d = largest_triangle_three_bucket(data,threshold,0,1)
    d = alternate_downsample_method(data,threshold,0,1)
    # format data for json
    df2 = pd.DataFrame(data = d)
    chart_data = df2.to_dict(orient='records')
    data = json.dumps(chart_data)
  
    return data

def alternate_downsample_method(data,threshold,x_property, y_property):
    # length of data that needs to be downsampled
    data_len = len(data)

    # if threshold is larger that the amount of data, return data
    if (threshold >= data_len):
        return data
    
    # bucket size. subtract two, must include first and last
    p = (data_len - 2) / (threshold - 2)

    
    # adding first point. 
    sampled = [data[0]]

    for i in range(0,threshold - 2):
        # range for the current bucket
        r_offs = int(math.floor((i + 0) * p) + 1)
        r_to = int(math.floor((i + 1) * p) + 1)
        print('range off',r_offs,'range to', r_to)

        # assume first value in range has the max/min tuple 
        max_tuple = data[r_offs]
        min_tuple = data[r_offs]
        y_max = -1
        y_min = data[r_offs][y_property]


        while r_offs < r_to:
            r_y = data[r_offs][y_property]
            if r_y > y_max:
                y_max = r_y
                max_tuple = data[r_offs]

            if r_y < y_min:
                y_min = r_y
                min_tuple = data[r_offs]
                
            r_offs += 1

        if min_tuple[x_property] < max_tuple[x_property]:
            sampled.append(min_tuple)
            sampled.append(max_tuple)
        elif min_tuple[x_property] == max_tuple[x_property]:
            print('EQUAL')
        else:
            sampled.append(max_tuple)
            sampled.append(min_tuple)

    # sample length should be ((threshold - 2) * 2) + 2
    sampled.append(data[data_len - 1])

    return sampled

def largest_triangle_three_bucket(data,threshold,x_property,y_property):
    
    # length of data that needs to be downsampled
    data_len = len(data)

    if (threshold >= data_len):
        # print("threshold not well defined")
        return data
    
    # bucket size. subtract two, must include first and last
    p = (data_len - 2) / (threshold - 2)
    # first pt in triangle
    a = 0
    max_area_point = (0,0)
    next_a = 0
    # adding first point. 
    sampled = [data[0]]

    for i in range(0,threshold - 2):
        # point avg for next bucket
        avg_x = 0
        avg_y = 0
        avg_range_start = int(math.floor((i + 1) * p) + 1)
        avg_range_end = int(math.floor((i + 2) * p) + 1)
        avg_rang_end = avg_range_end if avg_range_end < data_len else data_len

        avg_range_length = avg_rang_end - avg_range_start

        while avg_range_start < avg_rang_end:
            avg_x += data[avg_range_start][x_property]
            avg_y += data[avg_range_start][y_property]
            avg_range_start += 1

        avg_x /= avg_range_length
        avg_y /= avg_range_length

        # range for the current bucket
        r_offs = int(math.floor((i + 0) * p) + 1)
        r_to = int(math.floor((i + 1) * p) + 1)

        # pt a in the data 
        point_ax = data[a][x_property]
        point_ay = data[a][y_property]

        max_area = -1

        while r_offs < r_to:
            # triangle area of the three buckets 
            area = math.fabs(
                (point_ax - avg_x)
                * (data[r_offs][y_property] - point_ay)
                - (point_ax - data[r_offs][x_property])
                * (avg_y - point_ay)
            ) * 0.5

            if area > max_area:
                max_area = area
                max_area_point = data[r_offs]
                # next left most pt 'a' in next triangle is the 'b' point of cur triangle
                next_a = r_offs

            r_offs += 1
        # use the point with the largest area in triangle
        sampled.append(max_area_point)
        a = next_a

    # adding last pt in the data
    sampled.append(data[data_len - 1])

    return sampled
    

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')