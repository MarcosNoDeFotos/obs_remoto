# -*- coding: utf-8 -*-
ScriptName = "Besos Calva";
Website = "";
Description = "Cuenta los besos en la calva que llevo";
Creator = "MarcosNoDeFotos";
Version = "1.0.0";

COMANDO = "!calva";
datosCalva = "besos";

def enviarMensaje(mensaje):
    Parent.SendStreamMessage(mensaje);

def Init():
    return;

def Execute(data):
    besos = 0;
    with open(datosCalva) as f:
        besos = int(f.readlines()[0]);
    
    if data.GetParam(0) != COMANDO:
        return;
    username = data.UserName;
    besos = besos+1;
    f = open(datosCalva, "w");
    f.write(str(besos));
    f.close();
    enviarMensaje(username+" me ha dado un beso en la calva. Ya llevo "+str(besos)+" besos");
    return;

def Tick():
    return;
