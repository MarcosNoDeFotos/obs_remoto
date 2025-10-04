# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM

ScriptName = "LED Control";
Website = "";
Description = "Los usuarios pueden cambiar el color de los leds";
Creator = "MarcosNoDeFotos";
Version = "1.0.0";
Command = "!leds"
Cooldown = 30 #Segundos

coloresValidos = (
    "azuloscuro",
    "azulclaro",
    "rojo",
    "verde",
    "morado",
    "apagado",
    "random",
)



def enviarMensaje(mensaje):
    Parent.SendStreamMessage(mensaje);



def Init():
    
    return;

def Execute(data):
    if data.GetParam(0)!= Command:
        return;
    else:
        
        username = data.UserName;
        if data.GetParamCount() == 2:
            color = data.GetParam(1);
            if str(color).strip()!="help":
                colorEsHexa = True;
                try:
                    int(color[1:], 16);
                except:
                    colorEsHexa = False;
                if color in coloresValidos or (str(color).__len__()==7 and str(color)[0:1] == "#" and colorEsHexa):
                    if not Parent.IsOnCooldown(ScriptName,Command):
                        enviarColor(color); 
                    else:
                        enviarMensaje("Que me vas a fundir las luces!! Espérate un ratico (30s)");
                else:
                    enviarMensaje("Solo son válidos los colores azuloscuro, azulclaro, rojo, verde, morado, apagado, random (o color en formato hexadecimal #XXXXXX)");
            else:
                enviarMensaje("Usando el comando !leds seguido de un color (por ejemplo: !leds morado), puedes cambiarme el color del gorro! Los colores válidos son: azuloscuro, azulclaro, rojo, verde, morado, apagado, random (o color en formato hexadecimal #XXXXXX)");
        else:
            enviarMensaje(username+ ", el comando no es correcto!");
    
        
    return;

def Tick():
    return;

target_host = "192.168.1.144"
target_port = 80


def enviarColor(color):
    client = socket(AF_INET, SOCK_STREAM)  
    client.connect((target_host,target_port))  
    client.send(color.encode())  
    data = client.recv(1024)
       
    if str(data).strip()=="ok":
        Parent.AddCooldown(ScriptName,Command,Cooldown)
        enviarMensaje("Has cambiado el color de los leds!");
    else:
        enviarMensaje("Solo son válidos los colores azuloscuro, azulclaro, rojo, verde, morado, apagado, random (o color en formato hexadecimal #XXXXXX)");
    client.close();
