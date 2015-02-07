from flask import Flask
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
