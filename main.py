import serial
import time
import json
import requests
from remoteOBS import changeScene, initConnection, record, recording, stream, streaming
from _thread import start_new_thread
from flask import Flask, request, render_template, Response
import sqlite3
import threading


PUERTO_ARDUINO = "COM3"
DB_FILE = __file__.replace("main.py", "").replace("\\", "/")+"mensajesDestacados.db"


server_address = ('192.168.1.188', 8080)
serverReproductorSonido = "http://192.168.1.189:5000"
#server_address = ('192.168.1.189', 8080)


##########################################################


mostrarBotonPulsado = False


app = Flask("app")


# Init DB
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensajes_destacados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        mensaje TEXT NOT NULL
    )
""")
conn.commit()
conn.close()
# Init DB


config = {}
mensajesDestacar = []
lock = threading.Lock()

# Botones           = B (B1, B2, etc)
# Potenciómetros    = A (A0, A1, etc)
getOnlyButtons = [ 
    "B1",
    "B2",
    "B3",
    "B4",
    "B5",
    "B6",
    "B7",
    "B8",
    "B9",
    "B10",
    "B11",
    "B12",
    "B13",
    "B14",
    "B15",
    # "A0",
    # "A1",
    # "A2",
    # "A3",
]




currentPath = __file__.replace("main.py", "").replace("\\", "/")



def reproducirSonido(idSonido):
    with requests.Session() as s:
        s.get(serverReproductorSonido+"/reproducirSonido?identificador="+idSonido, timeout=10)
    

def reproducirSonidoCambiarEscena(data:str):
    idSonido = data.split(";")[0]
    escena = data.split(";")[1]
    delay = data.split(";")[2]
    start_new_thread(reproducirSonido, (idSonido,))
    time.sleep(float(delay))
    changeScene(escena)
    

def pararReproduccionSonido():
    with requests.Session() as s:
        s.get(serverReproductorSonido+"/pararReproduccionSonido", timeout=10)
    

def ensordecerDiscord():
    with requests.Session() as s:
        s.get(serverReproductorSonido+"/ensordecerDiscord", timeout=10)
    

def mutearDesmutearMicro():
    with requests.Session() as s:
        s.get(serverReproductorSonido+"/mutearDesmutearMicro", timeout=10)
    



def _key_detection():
    
    arduino = serial.Serial(PUERTO_ARDUINO, 9600)


    try:
        while True:
            rawString = arduino.readline()
            output = rawString.decode("utf-8").strip().replace("'", "")
            if output.__contains__("A"):
                pin = output.split("|")[0]
                value = output.split("|")[1]
                if pin in getOnlyButtons:
                    # TODO Acción de los potenciómetros
                    None
            elif output.__contains__("B"):
                buttonName = config["remap"][output]
                if mostrarBotonPulsado:
                    print(buttonName)
                elif buttonName in config["botones"].keys():
                    btnConfig =config["botones"][buttonName]
                    if btnConfig["accion"] == "escena":
                        changeScene(btnConfig["data"])
                    elif btnConfig["accion"] == "grabar":
                        record()
                    elif btnConfig["accion"] == "sonido":
                        start_new_thread(reproducirSonido, (btnConfig["data"],))
                    elif btnConfig["accion"] == "sonido_escena":
                        start_new_thread(reproducirSonidoCambiarEscena, (btnConfig["data"],))
                    elif btnConfig["accion"] == "stop_sonido":
                        start_new_thread(pararReproduccionSonido, ())
                    elif btnConfig["accion"] == "ensordecer":
                        start_new_thread(ensordecerDiscord, ())
                    elif btnConfig["accion"] == "mute":
                        start_new_thread(mutearDesmutearMicro, ())
                        None
                # if buttonName in acciones.keys():
                #     if acciones[buttonName] == GRABAR:
                #         record()
                #     elif acciones[buttonName] == STREAM:
                #         stream()
                #     elif acciones[buttonName] == MUTEAR:
                #         #TODO Mutear desmutear micro
                #         None
                
    except Exception as e:
        print(e)
        arduino.close()



def readConfig():
    global config
    try:
        with open(currentPath+"config.json", encoding="utf-8") as configFile:
            config = json.loads(configFile.read())
            configFile.close()
    except Exception as e:
        print("No se puede obtener la configuración")
        print(e)
        input("")
        exit(0)

def saveConfig():
    try:
        with open(currentPath+"config.json", "w", encoding="utf-8") as configFile:
            configFile.write(json.dumps(config))
            configFile.close()
    except Exception as e:
        print("No se puede guardar la configuración")
        print(e)
        input("")
        exit(0)





#Flask

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getConfigBotones")
def getConfigBotones():
    return json.dumps(config["botones"])

@app.route("/guardarConfigBoton", methods = ["POST"])
def guardarConfigBoton():
    id = request.form.get("id")
    accion = request.form.get("accion")
    data = request.form.get("data")
    global config
    if config["botones"].keys().__contains__(id):
        if accion != "none":
            config["botones"][id]["accion"] = accion
            config["botones"][id]["data"] = data
        else:
            config["botones"].pop(id)
    elif accion != "none":
        config["botones"][id] = {"accion" : accion, "data" : data}
    saveConfig()
    return json.dumps(config["botones"])



@app.route("/mensajesDestacados")
def mensajesDestacados():
    return render_template("mensajesDestacados.html")


@app.route("/destacarMensaje")
def destacarMensaje():
    usuario = request.args.get("user")
    mensaje = request.args.get("mensaje").strip()
    with lock:
        mensajesDestacar.append({"usuario": usuario, "mensaje": mensaje})
        # Mantener solo los últimos 50 mensajes
        if len(mensajesDestacar) > 50:
            mensajesDestacar.pop(0)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mensajes_destacados (usuario, mensaje) VALUES (?, ?)",(usuario, mensaje))
    conn.commit()
    conn.close()
    return {"status":"ok", "usuario": usuario, "mensaje": mensaje}


@app.route("/eliminarMensajeDestacado")
def eliminarMensajeDestacado():
    id = request.args.get("id")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mensajes_destacados where id = ?",(id,))
    conn.commit()
    conn.close()
    return {"status":"ok"}


@app.route('/streamMensajesDestacados')
def stream():
    def event_stream():
        last_index = 0
        while True:
            with lock:
                nuevos = mensajesDestacar[last_index:]
            for msg in nuevos:
                json_data = json.dumps(msg, ensure_ascii=False)
                yield f"data: {json_data}\n\n"
                last_index += 1
            time.sleep(0.1)  # pequeño delay para no saturar la CPU
    return Response(event_stream(), mimetype="text/event-stream")



@app.route('/getMensajesDestacados')
def getMensajesDestacados():
    """Devuelve todos los mensajes destacados en JSON"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario, mensaje FROM mensajes_destacados ORDER BY id ASC")
    filas = cursor.fetchall()
    conn.close()
    result = [{"id": fila[0], "usuario": fila[1], "mensaje": fila[2]} for fila in filas]
    return json.dumps(result)





if __name__ == '__main__':


    readConfig()
    while True: 
        if initConnection():
            print("Websocket conectado")
            break
        else:
            print("No se ha podido conectar por websocket. Reintentando en 5 segundos")
            time.sleep(5)
    start_new_thread(_key_detection, ())
    app.run(debug=False, host=server_address[0])
