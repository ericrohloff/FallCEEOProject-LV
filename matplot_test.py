import matplotlib.pyplot as plt
import js
from js import document, console
from widgets import UIElement
from pyodide.ffi import create_proxy
from pyodide.ffi.wrappers import add_event_listener
from pyscript import display


class InteractiveGraph:
    def __init__(self):
        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.points = []
        self.fig.set_size_inches(3, 2)

    def set_limits(self, xlim, ylim):
        # Set axis limits
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)

    def set_labels(self, xlabel, ylabel):
        # Set axis labels
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def set_title(self, title):
        # Set the title
        self.ax.set_title(title)

    def add_point(self, x, y):
        # Add a point to the graph
        self.points.append((x, y))

    def plot_points(self):
        # Plot the points on the graph
        if self.points:
            x, y = zip(*self.points)
            self.ax.plot(x, y, 'o', label='Points')

    def show_graph(self):
        # Show the graph
        self.plot_points()
        display(self.fig, target='test')


## TEST CODE ##

# from matplot_test import InteractiveGraph

# graph = InteractiveGraph()
# graph.set_limits((0, 10), (0, 10))
# graph.set_labels('X-axis', 'Y-axis')
# graph.set_title('Empty Graph')

# # Add points
# graph.add_point(3, 5)
# graph.add_point(6, 8)

# # Change the title
# graph.set_title('Graph with Points')

# # Show the graph with points
# graph.show_graph()
