import matplotlib.pyplot as plt
from pyscript import display
import js
from js import document


class InteractiveGraph:
    def __init__(self):
        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(3, 2)
        self.points = []

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
        # Clear the previous plot, if it exists
        self.clear_graph()
        self.plot_points()
        display(self.fig, target='plot')

    def clear_graph(self):
        # Clear the 'plot' div by setting its innerHTML to an empty string
        plot_div = js.document.getElementById('plot')
        if plot_div is not None:
            plot_div.innerHTML = ''

    def clear_data(self):
        # Clear the data points from the graph
        self.points = []
        js.console.log(self.points)

    def adjust_bounds(self, margin=0.1):
        # Automatically adjust the bounds of the graph based on data points
        if self.points:
            x, y = zip(*self.points)
            x_min, x_max = min(x), max(x)
            y_min, y_max = min(y), max(y)
            x_margin = (x_max - x_min) * margin
            y_margin = (y_max - y_min) * margin
            self.set_limits((x_min - x_margin, x_max + x_margin),
                            (y_min - y_margin, y_max + y_margin))
