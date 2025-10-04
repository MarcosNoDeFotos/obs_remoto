# -*- coding: utf-8 -*-
ScriptName = "Song Request";
Website = "";
Description = "Cuando alguien introduce el comando !request, se añade a la cola una canción";
Creator = "MarcosNoDeFotos";
Version = "1.0.0";

canciones = [];
def enviarMensaje(mensaje):
    Parent.SendStreamMessage(mensaje);

def Init():
    return;

def Execute(data):
    if data.GetParam(0)!= "!sr":
        return;
    else:
        username = data.UserName;
        cancion = "";
        for i in range(1, data.GetParamCount()):
            cancion+=data.GetParam(i)+" ";
        canciones.append(cancion);
        enviarMensaje(username+ " ha añadido la canción: "+cancion);
        Parent.Log("canciones actuales", canciones.__str__());
    return;

def Tick():
    return;
    