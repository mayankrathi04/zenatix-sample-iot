import csv
import cgi
import os
import random
from multiprocessing import Queue
import threading
from flask import Flask, request, jsonify, Response

print("Starting server...")

app = Flask(__name__)
data = Queue()


@app.route("/publish", methods=['POST'])
def publish():
    message = request.get_json()
    print(message)
    data.put(message)
    if(round(random.uniform(1,9))%3==0):
        return Response("{'status':'Not ok'}", status=400, mimetype='application/json')
    return Response("{'status':'Ok'}", status=200, mimetype='application/json')

def is_file_not_empty(file_path):
    return os.path.exists(file_path) and os.stat(file_path).st_size 

def dataSaver():
    fieldnames = ['Timestamp', 'Value', 'Sensor']
    if(not is_file_not_empty('sensor_data.csv')):
        print("Empty file")
        with open('sensor_data.csv', mode='a') as data_file:
            writer = csv.DictWriter(data_file, fieldnames=fieldnames)
            writer.writeheader()
    while(1):
        if(not data.empty()):
            with open('sensor_data.csv', mode='a') as data_file:
                writer = csv.DictWriter(data_file, fieldnames=fieldnames)
                m = data.get()
                writer.writerow({'Timestamp': m['time'], 'Value': m['data'], 'Sensor': m['name']})

dataSaverThread = threading.Thread(target=dataSaver)
dataSaverThread.start()
app.run(port=80)
