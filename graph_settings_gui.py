import gtk
import Gnuplot
import gui_components

class GraphSettingsGUI:

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
        self.baseVBox.show()

        self.titleBox = gui_components.LabelEntryBox("Title")
        self.baseVBox.add(self.titleBox.getHBox())

        self.xTitleBox = gui_components.LabelEntryBox("X-Axis Label")
        self.baseVBox.add(self.xTitleBox.getHBox())

        self.yTitleBox = gui_components.LabelEntryBox("Y-Axis Label")
        self.baseVBox.add(self.yTitleBox.getHBox())

        self.intervalsTitleBox = gui_components.LabelEntryBox("Set Interval Label")
        self.baseVBox.add(self.intervalsTitleBox.getHBox())
        
        self.font = gtk.ComboBox()
        self.fontLabel = gtk.Label("Font")
        self.fontBox = gtk.HBox()
        self.fontBox.add(self.fontLabel)
        self.fontBox.add(self.font)
        self.baseVBox.add(self.fontBox)
        self.font.show()
        self.fontLabel.show()
        self.fontBox.show()

        self.fontSize = gtk.ComboBox()
        self.fontSizeLabel = gtk.Label("Font Size")
        self.fontSizeBox = gtk.HBox()
        self.fontSizeBox.add(self.fontSizeLabel)
        self.fontSizeBox.add(self.fontSize)
        self.baseVBox.add(self.fontSizeBox)
        self.fontSize.show()
        self.fontSizeLabel.show()
        self.fontSizeBox.show()

        self.fontColor = gtk.ComboBox()
        self.fontColorLabel = gtk.Label("Font Color")
        self.fontColorBox = gtk.HBox()
        self.fontColorBox.add(self.fontColorLabel)
        self.fontColorBox.add(self.fontColor)
        self.baseVBox.add(self.fontColorBox)
        self.fontColor.show()
        self.fontColorLabel.show()
        self.fontColorBox.show()

        self.g = Gnuplot.Gnuplot(debug=1)

        self.g.title(self.titleBox.getEntry())
        self.g.plot('sin(x)')
        #raw_input('Please press return to continue...\n')

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
