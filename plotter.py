from matplot_test import InteractiveGraph
import js
from pyodide.ffi.wrappers import add_event_listener

graph = InteractiveGraph()
graph.set_limits((0, 10), (0, 10))
graph.set_labels('X-axis', 'Y-axis')
graph.set_title('Empty Graph')


def update_valuesX(event):
    global x_value
    x_element = js.document.getElementById("x")
    x_value = event.target.value
    x_element.value = x_value


def update_valuesY(event):
    global y_value
    y_element = js.document.getElementById("y")
    y_value = event.target.value
    y_element.value = y_value


def update_title(event):
    global title
    title_element = js.document.getElementById("title")
    title = event.target.value
    title_element.value = title


x = js.document.getElementById("x")
y = js.document.getElementById("y")
title = js.document.getElementById("title")
add_event_listener(x, "input", update_valuesX)
add_event_listener(y, "input", update_valuesY)
add_event_listener(title, "input", update_title)


def generator(event):
    x = js.document.getElementById("x")
    y = js.document.getElementById("y")
    title = js.document.getElementById("title")
    x = int(x.value)
    y = int(y.value)
    title = title.value
    graph.add_point(x, y)
    graph.set_title(title)
    graph.clear_graph()
    graph.show_graph()


def addpoint(event):
    x = js.document.getElementById("x")
    y = js.document.getElementById("y")
    x = int(x.value)
    y = int(y.value)
    graph.add_point(x, y)


def clear(event):
    graph.clear_graph()
    graph.set_title("Empty Graph")
    graph.clear_data()
    graph.show_graph()


generate = js.document.getElementById("generate")
addP = js.document.getElementById("init")
clear_button = js.document.getElementById("clear")
add_event_listener(generate, 'click', generator)
add_event_listener(addP, 'click', addpoint)
add_event_listener(clear_button, 'click', clear)
