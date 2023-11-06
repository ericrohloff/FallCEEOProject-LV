import matplotlib.pyplot as plt
import requests
from pyscript import display
from js import document
import js


class InteractiveGraph:
    def __init__(self):
        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(3, 2)  # Adjust the figure size
        self.points = []

    def set_limits(self, xlim, ylim):
        # Set axis limits
        if xlim[0] == xlim[1]:
            # Adjust the limits to avoid singularity
            xlim = (xlim[0] - 1, xlim[1] + 1)
        if ylim[0] == ylim[1]:
            ylim = (ylim[0] - 1, ylim[1] + 1)
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)

    def set_labels(self, xlabel, ylabel):
        # Set axis labels
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def set_title(self, title):
        # Set the title
        self.ax.set_title(title)

    def plot_points(self):
        # Plot the points on the graph
        if self.points:
            x, y = zip(*self.points)
            self.ax.plot(x, y, 'o', label='Points')
            self.adjust_bounds(0.1)
            self.show_graph()

    def add_point(self, x, y):
        # Add a point to the graph
        self.points.append((x, y))
        self.plot_points()

    def show_graph(self):
        # Clear the previous plot, if it exists
        plot = document.getElementById('plot')
        if plot is not None:
            plot.innerHTML = ''
        display(self.fig, target='plot')

    def clear_graph(self):
        plot = document.getElementById('plot')
        if plot is not None:
            plot.innerHTML = ''
        self.ax.clear()  # Clear the existing plot
        self.points = []  # Clear data
        self.set_title("Empty Graph")

    def adjust_bounds(self, margin):
        # Automatically adjust the bounds of the graph based on data points
        if self.points:
            x, y = zip(*self.points)
            x_min, x_max = min(x), max(x)
            y_min, y_max = min(y), max(y)
            x_margin = (x_max - x_min) * margin
            y_margin = (y_max - y_min) * margin
            self.set_limits((x_min - x_margin, x_max + x_margin),
                            (y_min - y_margin, y_max + y_margin))

    def zoom_out(self, margin):
        # Zoom out by adjusting the bounds with a larger margin
        self.adjust_bounds(margin)
        self.show_graph()
        js.console.log("zoom out")

    def zoom_in(self, margin):
        # Zoom in by adjusting the bounds with a smaller margin
        self.adjust_bounds(-margin)
        self.show_graph()  # Pass a negative margin to zoom in
        js.console.log("zoom in")
