from flask import Flask, send_file
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

app.run(threaded=True, host="0.0.0.0", port=getPort())