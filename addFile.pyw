from pathlib import Path
import PySimpleGUI as sg
import shelve
import random
import qrcode
import sys
import os

#-------------------#
ip = "localhost"
port = 5000
idLenght = 6
#-------------------#

abc = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z"
abc = abc + "," + abc.upper()
abc = abc.split(",")

sys.setrecursionlimit(99999)

def getPort() :
    return port

def genID(idLenght) :
    id = ""

    for i in range(idLenght) :
        id = id + random.choice(abc)

    return id

def getFullAddress(id, ip, port) :
    return "http://%s:%d/%s" % (ip, port, id)

def genQR(id, ip, port) :
    path = "%s.jpg" % (id)

    img = qrcode.make(getFullAddress(id, ip, port))
    img.save(path)

    return path

def addFile(file, idLenght) :
    file = os.path.abspath(file)

    if not os.path.isfile(file) :
        return ["Invalid path"]
    
    id = genID(idLenght)

    s = shelve.open("database")

    try :
        s[id]
        print("ID Already taken!")
        return addFile(file, idLenght+1) #ID Taken
    except KeyError :
        pass

    s[id] = file
    s.close()

    return ["ok", id]

def showQR(id, ip, port) :
    path = genQR(id, ip, port)

    layout = [[sg.Image(path)]]

    window = sg.Window('QR Code (%s)' % (id), layout, no_titlebar=False, keep_on_top=True, grab_anywhere=True, element_padding=(0,0))

    while True :
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Ok' :
            break
    
    try :
        os.remove(path)
    except :
        return "could not delete"
    
    return "ok"


def showAll(ip, port) :
    list = []

    s = shelve.open("database")
    for item in s :
        if not s[item] == "deleted" :
            list.append("%s - %s" % (item, s[item]))
    s.close()

    if list == [] :
        list = ["No files currently shared."]
        noItems = True
    else :
        noItems = False

    layout = [[sg.Listbox(list, size=(120,12), default_values=list[0])],
                [sg.Button("Show", disabled=noItems), sg.Button("Remove", disabled=noItems), sg.Stretch(), sg.Button("Close")]]

    window = sg.Window('All items', layout, no_titlebar=True, keep_on_top=True, grab_anywhere=True)

    while True :
        event, values = window.read()

        id = values[0][0].split(" -")[0]

        if event == "Remove" :
            s = shelve.open("database")
            s[id] = "deleted"
            s.close()
            
            window.close()
            return showAll(ip, port)

        if event == "Show" :
            window.close()
            successWindow(id, ip, port, False)
            return showAll(ip, port)
        
        if event == sg.WIN_CLOSED or event == 'Close' :
            break

    window.close()
    return "quit"

def successWindow(id, ip, port, allowShowAll) :
    layout = [[sg.Text('File share created!')],
            [sg.InputText(default_text=getFullAddress(id, ip, port), disabled=True)],
            [sg.Button('Ok'), sg.Button("Show QR Code"), sg.Stretch(), sg.Button("Show all", disabled=not allowShowAll)]]
    
    window = sg.Window('File share', layout, no_titlebar=True, keep_on_top=True, grab_anywhere=True)

    while True :
        event, values = window.read()

        if event == "Show QR Code" :
            print("Showing QR Code..")

            if showQR(id, ip, port) == "could not delete" :
                sg.popup("Could not delete the QR Code file!")
        
        if event == "Show all" :
            print("Showing all items..")
            window.close()
            showAll(ip, port)
            return successWindow(id, ip, port, allowShowAll)

        if event == sg.WIN_CLOSED or event == 'Ok' :
            break

    window.close()
    return "ok"

def chooseFileWindow() :
    layout = [[sg.FileBrowse(enable_events=True, button_text="Choose a file"), sg.InputText(disabled=True)],
                [sg.Button("Ok")]]

    window = sg.Window('Choose file', layout, no_titlebar=True, keep_on_top=True, grab_anywhere=True)

    while True :
        event, values = window.read()

        if event == "Ok" :
            window.close()
            return values[0]

        if event == sg.WIN_CLOSED or event == 'Ok' :
            window.close()
            return "quit"
def chooseFile() :
    path = chooseFileWindow()

    if not path == "quit" :
        out = addFile(path, idLenght)
        if out[0] == "ok" :
            successWindow(out[1], ip, port, True)
        else :
            print("ERROR: %s" % (out[0]))

if __name__ == "__main__" :
    args = sys.argv
    #print(args)

    if len(args) == 1 :
        chooseFile()
    else :
        os.chdir(os.path.dirname(args[0]))
        out = addFile(args[1], idLenght)

        if out[0] == "ok" :
            print(out[1])
            print(getFullAddress(out[1], ip, port))
            successWindow(out[1], ip, port, True)
        else :
            print("ERROR: %s" % (out[0]))