import gtk
#import Gnuplot
import gui_components

class GraphSettingsGUI:
    
    def hello():
        return False

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        #Recent Changes 1:56 PM Wednesday
        fontSizeList = ["10", "12", "14", "16", "18", "20", "22", "24",]
        fontTypeList = ["Arial", "Times New Roman", "Calibri", "Sans Serif", "Comic Sans"]
        fontColorList = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"]
        graphTypeList = ["Line", "Scatterplot", "Bar", "Pie Chart"]
        #
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
        
        self.font = gtk.ComboBox()
        #Additional Change Wednesday
        self.fontComboBox = gtk.combo_box_new_text()
        for x in range(0, 4):
            i = x
            j = x
            self.fontComboBox.insert_text(j, fontTypeList[i])
        self.fontComboBoxClicked = self.fontComboBox.get_active_text()
        
        #
        self.fontLabel = gtk.Label("Font")
        self.fontBox = gtk.HBox()
        self.fontBox.add(self.fontLabel)
        self.fontBox.add(self.font)
        self.baseVBox.add(self.fontBox)
        self.font.show()
        self.fontLabel.show()
        self.fontBox.show()

        self.fontSize = gtk.ComboBox()
        #Additional Change Wednesday
        self.fontSizeComboBox = gtk.combo_box_new_text()
        for x in range(0, 7):
            i = x
            j = x
            self.fontSizeComboBox.insert_text(j, fontSizeList[i])
        self.fontSizeComboBoxClicked = self.fontSizeComboBox.get_active_text()
        #
        self.fontSizeLabel = gtk.Label("Font Size")
        self.fontSizeBox = gtk.HBox()
        self.fontSizeBox.add(self.fontSizeLabel)
        self.fontSizeBox.add(self.fontSize)
        self.baseVBox.add(self.fontSizeBox)
        self.fontSize.show()
        self.fontSizeLabel.show()
        self.fontSizeBox.show()

        self.fontColor = gtk.ComboBox()
        #Additional Change Wednesday
        self.fontColorComboBox = gtk.combo_box_new_text()
        for x in range(0, 5):
            i = x
            j = x
            self.fontColorComboBox.insert_text(j, fontColorList[i])
        self.fontColorComboBoxClicked = self.fontColorComboBox.get_active_text()
        #
        self.fontColorLabel = gtk.Label("Font Color")
        self.fontColorBox = gtk.HBox()
        self.fontColorBox.add(self.fontColorLabel)
        self.fontColorBox.add(self.fontColor)
        self.baseVBox.add(self.fontColorBox)
        self.fontColor.show()
        self.fontColorLabel.show()
        self.fontColorBox.show()
        
        #Additional Changes Wednesday
        
        self.graphType = gtk.ComboBox()
        self.graphTypeComboBox = gtk.combo_box_new_text()
        for x in range(0, 3):
            i = x
            j = x
            self.graphTypeComboBox.insert_text(j, graphTypeList[i])
        self.graphTypeComboBoxClicked = self.graphTypeComboBox.get_active_text()
        self.graphTypeLabel = gtk.Label("Graph Type")
        self.graphTypeBox = gtk.HBox()
        self.graphTypeBox.add(self.graphTypeLabel)
        self.graphTypeBox.add(self.graphType)
        self.baseVBox.add(self.graphTypeBox)
        self.graphType.show()
        self.graphTypeLabel.show()
        self.graphTypeBox.show()
        
        
        self.dataParserButton = gtk.Button()
        self.dataParserButton.connect("clicked", self.hello, None) #   <---Not sure how to open data parser
        self.dataParserButtonLabel = gtk.Label("Open Data Parser")
        self.dataParserButtonBox = gtk.HBox()
        self.dataParserButtonBox.add(self.dataParserButtonLabel)
        self.dataParserButtonBox.add(self.dataParserButton)
        self.baseVBox.add(self.dataParserButtonBox)
        self.dataParserButton.show()
        self.dataParserButtonLabel.show()
        self.dataParserButtonBox.show()
        
        self.fileToParseEntry = gui_components.LabelEntryBox("Enter File Directory")
        self.baseVBox.add(self.fileToParseEntry.getHBox())
        
        self.graphItButton = gtk.Button()
        self.graphItButton.connect("clicked", self.hello, None) #   <---Not sure how to implement graphing
        self.graphItButtonLabel = gtk.Label("Graph It!")
        self.graphItButtonBox = gtk.HBox()
        self.graphItButtonBox.add(self.graphItButtonLabel)
        self.graphItButtonBox.add(self.graphItButton)
        self.baseVBox.add(self.graphItButtonBox)
        self.graphItButton.show()
        self.graphItButtonLabel.show()
        self.graphItButtonBox.show()
        #
        

        #self.g = Gnuplot.Gnuplot(debug=1)

        #self.g.title(self.titleBox.getEntry())
        #self.g.plot('sin(x)')
        
    

        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()


# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    hello = GraphSettingsGUI()
    hello.main()
