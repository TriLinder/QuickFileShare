from flask import Flask, send_file
from platform import system
from addFile import getPort
import shelve
import os

app = Flask(__name__)

@app.get("/<id>")
def getFile(id) :
    s = shelve.open("database")

    try :
        path = s[id]
    except KeyError :
        s.close()

        return "<b>Invalid ID</b>"
    
    if not os.path.isfile(path) or path == "deleted" :
        s[id] = "deleted"
        return "<b>Invalid ID</b>"
    
    return send_file(path)

if __name__ == "__main__" :
    if system() == "Windows" : #Hides the flask cmd window on Windows
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    app.run(threaded=True, host="0.0.0.0", port=getPort())