import js
from js import console
import asyncio
import pyodide
from pyodide.ffi import create_proxy
from pyodide.ffi.wrappers import add_event_listener
from pyscript import when
from widgets import *
from UITracker import UITracker
import serial


# Serial Functionality Set-Up
serial_button = js.document.getElementById('serial_button')
serial.SerialConsole("console")


async def connecter(event=None):
    id = js.document.getElementById("console")
    if id.style.visibility == "visible":
        id.style.visibility = "hidden"
    else:
        id.style.visibility = "visible"
    try:
        await serial.connect()
    except pyodide.ffi.JsException as e:
        console.log(f"Error: {e}")
        if "NotFoundError" in str(e):
            console.log("No port selected by the user.")
        else:
            console.log("Other error occurred.")
add_event_listener(serial_button, "click", connecter)
