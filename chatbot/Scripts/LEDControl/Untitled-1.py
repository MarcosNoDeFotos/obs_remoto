# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM

ScriptName = "LED Control";
Website = "";
Description = "Los usuarios pueden cambiar el color de los leds";
Creator = "MarcosNoDeFotos";
Version = "1.0.0";

coloresValidos = (
    "blanco",
    "azul",
)






def Init():
    return;
coloresValidos = (
    "azuloscuro",
    "azulclaro",
    "rojo",
    "verde",
    "morado",
    "apagado",
    "random",
)





def Tick():
    return;

target_host = "192.168.1.144"
target_port = 80


def enviarColor(color):
    client = socket(AF_INET, SOCK_STREAM)  
    client.connect((target_host,target_port))  
    client.send(color.encode())  
    data = client.recv(4096)
    if data:
        datos=bytes.decode(data)
        print(datos);       
       
    client.close();
color = "#0000fA"
colorEsHexa = True;
try:
    int(color[1:], 16);
except:
    colorEsHexa = False;
#if color in coloresValidos:
if color in coloresValidos or (str(color).__len__()==7 and str(color)[0:1] == "#" and colorEsHexa):
    enviarColor(color); 