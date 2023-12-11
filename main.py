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


def getButton(idx):
    return tracker.getWidget(buttonWidget, idx)


def getLed(idx):
    return tracker.getWidget(LEDWidget, idx)


@when("click", selector=".widget-adder__button")
def toggleButtonAdderMenu(evt):
    evt.currentTarget.parentElement.querySelector(
        ".widget-adder__menu").classList.toggle("shown")


@when("click", selector=".headBar__tab")
def toggleFrontPanel(evt):
    # find which tab was clicked and its associated page
    targetPage = evt.currentTarget.getAttribute("data-page-target")
    # loop through pages and hide them, but show the target page
    for page in js.document.querySelectorAll(".pageContent__content"):
        if page.getAttribute("data-page") == targetPage:
            page.classList.add("shown")
        else:
            page.classList.remove("shown")

    # remove selected style from previously selected tab and add to new one
    for tab in js.document.querySelectorAll(".headBar__tab"):
        if tab == evt.currentTarget:
            tab.classList.add("selected")
        else:
            tab.classList.remove("selected")
