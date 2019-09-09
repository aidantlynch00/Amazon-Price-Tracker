from tkinter import *
import numpy as np

class APT_Graph:

    def __init__(self, x, y, width, height, grid_size, master = None, init_data = None):
        #Save parameters to class
        self.width, self.height, self.grid_size = width, height, grid_size
        self.xoff = 100
        self.dates, self.prices = [], []
        self.available = True
        #Amount of points that can fit on the graph
        self.dates_available = int((self.width - self.xoff * 2) / self.grid_size) + 1

        #Init graph canvas
        self.canvas = Canvas(master = master, width = width, height = height + 50)
        self.canvas.configure(background = "white")
        self.canvas.pack()

        #Create new window on master canvas to house the graph canvas
        master.create_window(x, y, anchor = "nw", window = self.canvas)

        if init_data is not None:
            self.add_data(init_data)

        self.draw_graph()


    def draw_graph(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_points()


    def draw_grid(self):
        for i in range(self.dates_available):
            x = i * self.grid_size + self.xoff
            self.canvas.create_line(x, 0, x, self.height)  

        self.canvas.create_line(self.xoff, self.height, self.width - self.xoff, self.height)


    def draw_points(self):
        for i in range(self.dates_available):
            if i > len(self.dates) - 1: 
                return
            
            price = self.prices[i]
            x = i * self.grid_size + self.xoff
            y = self.get_y(price)
            self.canvas.create_line(self.xoff, y, x, y, dash = (5, 5))
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill = "orange", outline = "black")
            self.canvas.create_text(x, self.height + 10, justify = "center", text = str(self.dates[i]))
            price_str = "$" + str(price)
            self.canvas.create_text(self.xoff - 5 * (len(price_str) - 1), y, justify = "left", text = price_str)


    def update_data(self, data):
        if len(data) == 0: return
        self.dates = []
        self.prices = []

        #Data comes in as a list of tuples from SQL DB
        for i in range(len(data)):
            self.dates.append(data[i][0])
            self.prices.append(data[i][1])

        #Segment data to pull the %dates_available% most current data points
        self.dates = self.dates[:self.dates_available]
        self.prices = self.prices[:self.dates_available]
        self.available = bool(data[-1][2])


    def get_y(self, price):
        min_price = min(self.prices)
        max_price = max(self.prices)

        if min_price == max_price:
            min_price = 0

        y = (price - min_price) / (max_price - min_price) * ((self.height - 25) - 25) + 25
        return self.height - y
