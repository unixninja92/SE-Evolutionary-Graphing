__author__ = 'thomasguttman'


filenames = #parsed data to be plotted
graphsettings = #customized graph settings

from matplotlib.pyplot import *
import pylab

datalist = [ ( pylab.loadtxt(filename), label ) for filename, label in list_of_files ]

for data, label in datalist:
    pylab.plot( data[:,0], data[:,1], label=label )

pylab.legend()
pylab.title("Title of Plot")
pylab.xlabel("X Axis Label")
pylab.ylabel("Y Axis Label")
pylab.show()

plt.savefig('sine_function_plain.png')#saves the figure in a seperate file



def save_graph_settings():

def apply(graphSettings):#create new graph from graph settings  .gettext
