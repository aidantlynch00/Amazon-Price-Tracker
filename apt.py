'''This file initializes the GUI of the tracker and all necessary components for file IO'''

import numpy as np
#import matplotlib as mpl
import os
from time import sleep
from tkinter import *
#import matplotlib.backends.tkagg as tkagg
#from matplotlib.backends.backend_agg import FigureCanvasAgg
from apt_graph import APT_Graph
import apt_connector

class Application(Frame):

    def __init__(self, master = None):
        super().__init__(master, bg = "white")
        self.master = master

        #Configure window
        self.master.geometry("1600x900")
        self.master.title("Amazon Price Tracker")
        self.master.configure(background = "white")
        self.pack()

        #Create widgets
        self.init_widgets()


    def init_widgets(self):
        #Define Canvas
        self.canvas = Canvas(self, width = 1600, height = 900)
        self.canvas.configure(background = "white")
        self.canvas.pack()

        #Place logo on Canvas
        path = os.getcwd() + "\\apt_icon.png"
        logo = PhotoImage(file = path)
        self.canvas.create_image(500, 0, image = logo, anchor = "nw")
        self.canvas.image = logo #Avoid python garbage collection from scooping up my img

        #Place graph on canvas
        self.graph = APT_Graph(50, 125, 1500, 350, 130, master = self.canvas) # , init_data = apt_connector.get_data("sony_headphones_b07g4mnfs1")
        #graph.add_data(apt_connector.get_data("sony_headphones_b07g4mnfs1"))
        self.canvas.graph = self.graph #Again :P


    def update_graph(self, table_name):
        self.graph.update_data(apt_connector.get_data(table_name))
        self.graph.draw_graph()



#Init DB connector
apt_connector = apt_connector.APT_Connector("amazon_price_tracker")

#Init Window and App
root = Tk()
app = Application(master = root)

#Run the application
#app.mainloop()
#app.update_graph("sony_headphones_b07g4mnfs1")

while True:
    app.after(10, app.update_graph("sony_headphones_b07g4mnfs1"))
    app.update_idletasks()
    app.update()













#self.canvas.create_line(0, 0, 800, 600)
        #main_label = Label(self.canvas, text = "Amazon Price Tracker", font = ("Courier New", 32), bg = "black", fg = "red")
        #main_label.pack({"side": "top"})


#MPL in Tkinter
'''
def embed_graph(canvas, graph, location = (0, 0)):
    #Init graph canvas
    graph_canvas = FigureCanvasAgg(graph)
    graph_canvas.draw()
    graph_x, graph_y, graph_width, graph_height = graph.bbox.bounds
    #Convert width and height to usable integers
    graph_width, graph_height = int(graph_width), int(graph_height)

    #Create an image background for the mpl graph
    graph_image = PhotoImage(master = canvas, width = graph_width, height = graph_height)
    canvas.create_image(location[0] + graph_width / 2, location[0] + graph_height / 2, image = graph_image)
    #Assign a renderer to the graph canvas
    tkagg.blit(graph_image, graph_canvas.get_renderer()._renderer, colormode = 2)

    return graph_image #Avoid garbage collection because python sucks ;)

def draw_graph(self, graph, location = (0, 0)):
    graph_image = self.embed_graph(self.canvas, graph, location = location)



graph = mpl.figure.Figure(figsize = (2, 1))
axes = graph.add_axes([0, 0, 1, 1])
axes.plot(np.linspace(0, 100), 50)

app.draw_graph(graph, location = (0, 0))
'''