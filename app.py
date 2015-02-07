from flask import Flask, abort, Response
import csv
import json
import os

app = Flask(__name__)

def find_by_field_value(array, field, value):
    for item in array:
        if field in item and str(item[field]) == str(value):
            return item
    return None

def dict_for_field(data, field):
    if not data or not field or not field in data:
        return None
    json = {}
    json[field] = data[field]
    return json

cache = {}

def read_csv(f):
    out = []
    if f in cache:
        out = cache[f]
    if not out:
        with open(f) as data:
            reader = csv.reader(data)
            keys = []
            read_keys = False
            idx = 0
            for row in reader:
                if not read_keys:
                    keys = [key.lower() for key in row]
                    if not 'id' in keys:
                        keys.append('id')
                    read_keys = True
                else:
                    data = {}
                    for i in range(len(row)):
                        data[str(keys[i])] = row[i]
                    if not 'id' in data:
                        data['id'] = idx
                    out.append(data)
                    idx += 1
        cache[f] = out
    return out

def format_row_data(data):
    return data;

def json_response(data):
    return Response(json.dumps(data), content_type='application/json; charset=utf-8')

def add_hal_links(item, controller, data):
    link_self = "/" + controller + "/" + data + "/" + str(item['id'])
    item['_links'] = {"self": {"href": link_self}}


@app.route('/')
def index():
    response = {'_embedded':{}}
    resources = []
    for res in os.listdir('data'):
        obj = {}
        obj['name'] = res
        obj['_links'] = {'self':{'href': '/' + res}}
        resources.append(obj)
    response['_embedded']['resources'] = resources
    return json_response(response)

@app.route('/<controller>')
def controller(controller):
    response = {'_embedded':{}}
    resources = []
    for res in os.listdir('data/' + controller):
        obj = {}
        obj['name'] = res.split('.')[0]
        obj['_links'] = {'self':{'href': '/' + controller + '/' + res.split('.')[0]}}
        resources.append(obj)
    response['_embedded']['resources'] = resources
    return json_response(response)

@app.route('/<controller>/<data>')
@app.route('/<controller>/<data>/<identity>')
@app.route('/<controller>/<data>/<identity>/<field>')
def handle(controller, data, identity=None, field=None):
    f = "data/" + controller + "/" + data + ".csv"
    if not os.path.exists(f):
        abort(404)
    csv = read_csv(f)
    if not identity and not field:
        for item in csv:
            add_hal_links(item, controller, data)
        response = {'_links':{'self':{'href': '/' + controller + '/' + data}}, 'size': len(csv), '_embedded': csv}
        return json_response(response)
    item = {}
    if identity:
        item = find_by_field_value(csv, 'id', identity)
        if not item:
            abort(404)
    if not field:
        add_hal_links(item, controller, data)
        return json_response(item)
    else:
        out = dict_for_field(item, field)
        if out:
            add_hal_links(item, controller, data)
            return json_response(out)
        else:
            abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
