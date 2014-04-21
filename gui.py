import gtk
import Gnuplot

def create_window():
    window = gtk.Window()
    window.set_default_size(200, 200)
    window.connect('destroy', gtk.main_quit)
    
    window.show()
 
create_window()
gtk.main()
