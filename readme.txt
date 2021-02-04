Requirements:
Python 3.8.5

Steps to run:
1)To run server:
python server.py

2)To run edge
python edge.py


Overview
Server is build on flask and runs on localhost with port 80
    Endpoint:"/publish" Type:POST
    Accepts:JSON Type:{'time':string,'data':decimal,'name':string}
    Response:
        Correct:Status Code:200 , {'status':'Ok'}
        Wrong:Status Code:400 , {'status:'Not ok'}
For simulation 66% request is allowed and 33% are rejected