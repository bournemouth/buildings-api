from flask import Flask
from flask import abort
import csv
import json

app = Flask(__name__)

@app.route('/services/police')
def police():
    return json.dumps(read_csv('data/services/police.csv'))

@app.route('/services/fire')
def fire():
    return json.dumps(read_csv('data/services/fire.csv'))

@app.route('/services/ambulance')
def amulance():
    return json.dumps(read_csv('data/services/ambulance.csv'))

@app.route('/services/lifeboat')
def lifeboat():
    return json.dumps(read_csv('data/services/lifeboat.csv'))

@app.route('/services/coastguard')
def coastguard():
    return json.dumps(read_csv('data/services/coastguard.csv'))

@app.route('/buildings/listed')
def buildings_listed():
    return json.dumps(read_csv('data/buildings/listed.csv'))

@app.route('/buildings/listed/<int:building_id>')
def buildings_listed_by_index(building_id):
    data = read_csv('data/buildings/listed.csv')
    for building in data:
        if int(building['id']) == building_id:
            return json.dumps(building)
    abort(404)

@app.route('/buildings/listed/<int:building_id>/<field>')
def get_building_field_by_id(building_id, field):
    data = read_csv('data/buildings/listed.csv')
    building = None
    for b in data:
        if int(b['id']) == building_id:
            building = b
            break
    if not building:
        abort(404)
    if field in building:
        wrap = {}
        wrap[field] = building[field]
        return json.dumps(wrap)
    else:
        abort(404)

def read_csv(f):
    out = []
    with open(f) as data:
        reader = csv.reader(data)
        keys = []
        read_keys = False
        for row in reader:
            if not read_keys:
                keys = [key.lower() for key in row]
                read_keys = True
            else:
                data = {}
                i = 0
                for value in row:
                    data[str(keys[i])] = value
                    i += 1
                out.append(data)
    return out

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
