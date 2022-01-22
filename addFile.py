import PySimpleGUI as sg
import shelve
import random
import os

abc = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z"
abc = abc + "," + abc.upper()
abc = abc.split(",")

def genID(idLenght) :
    id = ""

    for i in range(idLenght) :
        id = id + random.choice(abc)

    return id

def addFile(file, idLenght) :
    if not os.path.isfile(file) :
        return ["not a file"]
    
    s = shelve.open("database")
    s[""]