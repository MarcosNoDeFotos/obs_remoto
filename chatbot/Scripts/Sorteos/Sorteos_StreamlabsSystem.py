# -*- coding: utf-8 -*-
import json
import os
import codecs
from datetime import datetime;

ScriptName = "Sorteo";
Website = "";
Description = "Los espectadores pueden participar en el sorteo con un comando";
Creator = "MarcosNoDeFotos";
Version = "1.0.0";
settings = {};
participantes = [];
sorteoActivo = False;
comando = "";


def enviarMensaje(mensaje):
    Parent.SendStreamMessage("/me "+mensaje);
    return;


def leerConfigJSON():
    work_dir = os.path.dirname(__file__);
    with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as config_file:
        return json.load(config_file, encoding='utf-8-sig');


def exportarParticipantes():
    global participantes;
    global settings;
    participantesTexto = "";
    for p in participantes:
        participantesTexto+=p+";";
    with open(settings['ruta_exportacion_fichero']+"/participantes-"+datetime.now().strftime("%d-%m-%Y-%H%M%S")+".csv", "w") as f:
        f.write(participantesTexto[:participantesTexto.__len__()-1]);

def Init():
    global settings;
    settings = leerConfigJSON();    
    #Parent.Log("!sorteo", settings['comando_ver_objeto_sorteo']+", "+settings['participar']+", "+settings['objeto_sorteo'])
    return;

def Execute(data):
    global sorteoActivo;
    username = data.UserName;
    param0 = data.GetParam(0);
    if param0 == "!"+settings['participar']:
        if not sorteoActivo:
            enviarMensaje("El sorteo ya no está activo, no puedes participar :(");
        else:
            if username not in participantes:
                participantes.append(data.UserName);
                enviarMensaje(data.UserName+", ¡Has entrado en el sorteo!");    
            else:
                enviarMensaje(data.UserName+", ya estás en el sorteo :D");    
    elif param0 == "!"+settings['comando_ver_objeto_sorteo']:
        enviarMensaje("Se está sorteando: "+settings['objeto_sorteo']+". Hay "+str(participantes.__len__())+" participante(s)");
    elif param0 == "!"+settings['comando_parar_sorteo'] and Parent.HasPermission(data.User, settings['permisos_administracion'], ""):
        sorteoActivo = False;
        enviarMensaje("**El sorteo ha finalizado**. Ya no pueden participar más personas");
        exportarParticipantes();
    elif param0 == "!"+settings['comando_reanudar_sorteo']  and Parent.HasPermission(data.User, settings['permisos_administracion'], ""):
        sorteoActivo = True;
        enviarMensaje("**Se ha reanudado el sorteo**. Podéis volver a participar usando el comando !"+settings['participar']);
    elif param0 == "!"+settings['comando_cambiar_objeto_sorteo'] and Parent.HasPermission(data.User, settings['permisos_administracion'], ""):
        objeto = "";
        for i in range(1, data.GetParamCount()):
            objeto+=data.GetParam(i)+" ";
        settings['objeto_sorteo'] = objeto;
        enviarMensaje("Ahora se está sorteando: "+settings['objeto_sorteo']);
    return;

def Tick():
    return;
    