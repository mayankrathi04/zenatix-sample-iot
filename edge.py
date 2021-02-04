import time
from multiprocessing import Queue
import threading
import random
import requests
from datetime import datetime


class Counter:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = 0

    def inc(self):
        with self.lock:
            self.value += 1

    def getCount(self):
        with self.lock:
            return self.value


class Edge:
    def __init__(self):
        self.buff = Queue()
        self.successCounter = Counter()

    #function for simulation of sending sensor data
    def simulate(self):
        while(1):
            t1 = time.time()
            while(time.time()-t1 < 60):
                pass
            sd = self.getRandomSensorData()
            print("Sending sensor data:", sd)
            self.sendReq(sd)
        
    #function for simulation of sending buffered sensor data
    def sendBufferedData(self):
        while(1):
            t1 = time.time()
            while(time.time()-t1 < 5):
                pass
            while(not self.buff.empty()):
                print("Sending buffered data")
                sd = self.buff.get()
                self.sendReq(sd)
                break

    def sendReq(self, sd):
        try:
            r = requests.post(url="http://localhost:80/publish", json=sd)
            print("Got Response:", r.status_code, " ", r.text)
            if(r.status_code != 200):
                self.buff.put(sd)
            if(r.status_code == 200):
                self.successCounter.inc()
        except Exception as e:
            print(e)

    def getSuccessCounter(self):
        return self.successCounter.getCount()

    def getBufferedDataCount(self):
        return self.buff.qsize()

    def clientStart(self):
        t1 = threading.Thread(target=self.simulate)
        t2 = threading.Thread(target=self.sendBufferedData)
        t1.start()
        t2.start()

    def getRandomSensorData(self):
        v1 = round(random.uniform(31, 40), 2)
        dateTimeObj = datetime.now()
        v2 = str(dateTimeObj.year) + '/' + str(dateTimeObj.month) + '/' + str(dateTimeObj.day) + \
            "T"+str(dateTimeObj.hour) + ':' + \
            str(dateTimeObj.minute) + ':'+str(dateTimeObj.second)
        v3 = "Sensor-2"
        return({"data": v1, "time": v2, "name": v3})


e1 = Edge()
e1.clientStart()
