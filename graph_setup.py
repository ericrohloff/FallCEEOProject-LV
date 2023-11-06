from interactive_graph import InteractiveGraph
import js
from pyodide.ffi.wrappers import add_event_listener

graph = InteractiveGraph()
graph.set_limits((0, 10), (0, 10))
graph.set_labels('X-axis', 'Y-axis')
graph.set_title('Empty Graph')
graph.show_graph()


def clear(event):
    graph.clear_graph()
    graph.show_graph()


def title(event):
    new_title = js.document.getElementById("title")
    new_title = event.target.value
    graph.set_title(new_title)
    graph.show_graph()


def zoom_out(event):
    graph.zoom_out(0.4)
    graph.show_graph()


def zoom_in(event):
    graph.zoom_in(0.4)
    graph.show_graph()


# Event Listener Setup
clear_button = js.document.getElementById("clear")
zoom_out_button = js.document.getElementById("out")
zoom_in_button = js.document.getElementById("in")
add_event_listener(clear_button, 'click', clear)
add_event_listener(js.document.getElementById("title"), 'input', title)
add_event_listener(zoom_out_button, 'click', zoom_out)
add_event_listener(zoom_in_button, 'click', zoom_in)
