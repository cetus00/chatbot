from flask import Flask,request,abort
from datetime import datetime
import time

app = Flask(__name__)
messages = [
    {'name':"John", 'time':time.time(),'text':"asasdfasdf"},
    {'name':"John", 'time':time.time(),'text':"asasdfasdf"},
    {'name':"Nick", 'time':time.time(),'text':"hi all!"},
    {'name':"John", 'time':time.time(),'text':"Hi there, Nick"},
    {'name':"orca", 'time':time.time(),'text':"hi all! I am an orca"},

]

users = {'John':'12345', 'Nick':'qwerty','orca':'orca'}

@app.route("/")
def hello_view():
    return "Hello, World! <a href = '/status'>Статус</a>"

@app.route("/status")
def status_view():

    return {
        "status":True,
        "name":"TEST",
        "time":datetime.now().strftime("Hi! Current time is %Y/%m/%d %H-%M-%S"),
        "total_messages":len(messages),
        "total_users":len(users)
    }

@app.route("/send",methods=['POST'])
def send_view():
    name = request.json.get("name") #if name in json, return name else None
    text = request.json.get("text")
    password = request.json.get('password')

    for token in [name,password,text]:
        if not isinstance(token,str) or not 0 < len(token) <=1024:
            abort(400) #bad request

    if name in users:
        #auth
        if users[name] != password:
            abort(401)
    else:
        #sign up
        users[name] = password

    messages.append({'name':name,"text":text,"time":time.time()})
    return Response(status=200)

def filter_dicts(elements,key,min_value):
    new_elements = []
    for element in elements:
        if element[key]>min_value:
            new_elements.append(element)
    return new_elements

@app.route("/messages")
def messages_view():
    try:
        after = float(request.args['after'])
    except:
        abort(400)

    filtered_messages = filter_dicts(messages,key='time',min_value=after)
    return {"messages":filtered_messages}

app.run()
