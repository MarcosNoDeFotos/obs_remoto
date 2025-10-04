from time import sleep
from obswebsocket import obsws, requests

websocket = None;
password = "OWuiX3yGP5vjqZDB"
host = "192.168.1.188"
port = "4455";


streaming = False;
recording = False;



def initConnection():
    global websocket;
    try:
        websocket = obsws(host=host, port=port);
        websocket.connect();
        return True;
    except:
        return False;



def changeScene(name):
    req = requests.SetCurrentProgramScene(sceneName=name)
    websocket.call(req)




def record():
    if recording:
        stopRecording();
    else:
        startRecording();


def stream():
    if streaming:
        stopStream();
    else:
        startStream();



def startStream():
    global streaming;
    try:
        websocket.call(requests.StartStreaming());
        streaming = True;
    except Exception as e:
        print(e);
        streaming = False;

def stopStream():
    global streaming;
    try:
        websocket.call(requests.StopStreaming());
        streaming = False;
    except Exception as e:
        print(e);
        streaming = True;




def startRecording():
    global recording;
    try:
        websocket.call(requests.StartRecord());
        sleep(0.3);
        recording = True;
    except Exception as e:
        print(e);
        recording = False;

def stopRecording():
    global recording;
    try:
        websocket.call(requests.StopRecord());
        sleep(0.3);
        recording = False;
    except Exception as e:
        print(e);
        recording = True;


