from flask import Flask, abort, Response
import csv
import json
import os
import re

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
                        data[str(keys[i])] = format_row_data(row[i])
                    if not 'id' in data:
                        data['id'] = idx
                    out.append(data)
                    idx += 1
        cache[f] = out
    return out


def format_row_data(data):
    if re.search('^[A-Z0-9\ \,\.]*$', data):
        data = data.title()
    return data;

def json_response(data):
    return Response(json.dumps(data), content_type='application/json; charset=utf-8')

@app.route('/<controller>/<data>')
@app.route('/<controller>/<data>/<identity>')
@app.route('/<controller>/<data>/<identity>/<field>')
def handle(controller, data, identity=None, field=None):
    f = "data/" + controller + "/" + data + ".csv"
    if not os.path.exists(f):
        abort(404)
    csv = read_csv(f)
    if not identity and not field:
        return json_response(csv)
    item = {}
    if identity:
        item = find_by_field_value(csv, 'id', identity)
        if not item:
            abort(404)
    if not field:
        return json_response(item)
    else:
        out = dict_for_field(item, field)
        if out:
            return json_response(out)
        else:
            abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
