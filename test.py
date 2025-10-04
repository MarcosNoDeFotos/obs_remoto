import serial
import time
import json
import requests
from remoteOBS import changeScene, initConnection, record, recording, stream, streaming
from _thread import start_new_thread
from flask import Flask, request, render_template




PUERTO_ARDUINO = "COM3"
arduino = serial.Serial(PUERTO_ARDUINO, 9600)


try:
    while True:
        rawString = arduino.readline()
        output = rawString.decode("utf-8").strip().replace("'", "")
        print(output)
except Exception as e:
    print(e)
    arduino.close()
