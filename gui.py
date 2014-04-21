import gtk
import Gnuplot

class GUI:

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.baseVBox = gtk.VBox()
        self.window.add(self.baseVBox)
        self.show()

        self.hbox1 = gtk.HBox()
        self.baseVBox.add(self.hbox1)
        self.hbox1.show()
        
        self.label1 = gtk.Label("label1")
        self.hbox1.add(self.label1)
        self.label1.show()

        self.entry1 = gtk.Entry()
        self.hbox1.add(self.entry1)
        self.entry1.show()

        # Creates a new button with the label "Hello World".
        #self.button = gtk.Buttoton("Hello World")
    
        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        #self.button.connect("clicked", self.hello, None)
    
        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        #self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
    
        # This packs the button into the window (a GTK container).
        #self.window.add(self.button)
    
        # The final step is to display this newly created widget.
        #self.button.show()
    
        # and the window
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    hello = GUI()
    hello.main()
