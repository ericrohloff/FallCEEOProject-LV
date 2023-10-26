import js
from pyodide.ffi import create_proxy
from widgets import *

class storeInfo:
    def __init__(s):
        s.sendReceive("hello", "goodbye")

    def sendReceive(send, receive):
        print(js.localStorage.getItem(receive))
        js.localStorage.setItem(send, send)
        print(js.localStorage.getItem(send))
        print("hello world")
        js.localStorage.removeItem(send)
    

    def LEDStoreInfo(state):
        js.localStorage.setItem("LED", state)
    
    def LEDGetInfo():
        return js.localStorage.getItem("LED")
    
    
