import gtk
import gui_components
#import graphsettings

class GraphSettingsGUI:
    
    def hello():
        return False

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        fontSizeList = ["10", "12", "14", "16", "18", "20", "22", "24",]
        fontTypeList = ["Arial", "Times New Roman", "Calibri", "Sans Serif", "Comic Sans"]
        fontColorList = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"]
        graphTypeList = ["Line", "Scatterplot", "Bar", "Pie Chart"]
        #
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        
        self.baseHBoxForVBox = gtk.HBox()
        self.window.add(self.baseHBoxForVBox)
        self.baseHBoxForVBox.show()
        self.baseVBox = gtk.VBox()
        self.baseHBoxForVBox.add(self.baseVBox)
        self.baseVBox.show()
        self.baseVBox2 = gtk.VBox()
        self.baseHBoxForVBox.add(baseVBox2)
        self.baseVBox2.show()

        self.titleBox = gui_components.LabelEntryBox("Title")
        self.baseVBox.add(self.titleBox.getHBox())

        self.xTitleBox = gui_components.LabelEntryBox("X-Axis Label")
        self.baseVBox.add(self.xTitleBox.getHBox())

        self.yTitleBox = gui_components.LabelEntryBox("Y-Axis Label")
        self.baseVBox.add(self.yTitleBox.getHBox())
        
        #self.font = gtk.ComboBox()
        #Additional Change Wednesday
        self.fontComboBox = gtk.combo_box_new_text()
        for x in range(0, 5):
            i = x
            j = x
            self.fontComboBox.insert_text(j, fontTypeList[i])
        self.fontComboBoxEntry = self.fontComboBox.get_active_text()
        
        #
        self.fontLabel = gtk.Label("Font")
        self.fontBox = gtk.HBox()
        self.fontBox.add(self.fontLabel)
        self.fontBox.add(self.fontComboBox)
        self.baseVBox.add(self.fontBox)
        self.fontComboBox.show()
        self.fontLabel.show()
        self.fontBox.show()

        #self.fontSize = gtk.ComboBox()
        #Additional Change Wednesday
        self.fontSizeComboBox = gtk.combo_box_new_text()
        for x in range(0, 8):
            i = x
            j = x
            self.fontSizeComboBox.insert_text(j, fontSizeList[i])
        self.fontSizeComboBoxEntry = self.fontSizeComboBox.get_active_text()
        #
        self.fontSizeLabel = gtk.Label("Font Size")
        self.fontSizeBox = gtk.HBox()
        self.fontSizeBox.add(self.fontSizeLabel)
        self.fontSizeBox.add(self.fontSizeComboBox)
        self.baseVBox.add(self.fontSizeBox)
        self.fontSizeComboBox.show()
        self.fontSizeLabel.show()
        self.fontSizeBox.show()

        #self.fontColor = gtk.ComboBox()
        #Additional Change Wednesday
        self.fontColorComboBox = gtk.combo_box_new_text()
        for x in range(0, 6):
            i = x
            j = x
            self.fontColorComboBox.insert_text(j, fontColorList[i])
        self.fontColorComboBoxEntry = self.fontColorComboBox.get_active_text()
        #
        self.fontColorLabel = gtk.Label("Font Color")
        self.fontColorBox = gtk.HBox()
        self.fontColorBox.add(self.fontColorLabel)
        self.fontColorBox.add(self.fontColorComboBox)
        self.baseVBox.add(self.fontColorBox)
        self.fontColorComboBox.show()
        self.fontColorLabel.show()
        self.fontColorBox.show()
        
        #Additional Changes Wednesday
        
        #self.graphType = gtk.ComboBox()
        self.graphTypeComboBox = gtk.combo_box_new_text()
        for x in range(0, 4):
            i = x
            j = x
            self.graphTypeComboBox.insert_text(j, graphTypeList[i])
        self.graphTypeComboBoxEntry = self.graphTypeComboBox.get_active_text()
        self.graphTypeLabel = gtk.Label("Graph Type")
        self.graphTypeBox = gtk.HBox()
        self.graphTypeBox.add(self.graphTypeLabel)
        self.graphTypeBox.add(self.graphTypeComboBox)
        self.baseVBox.add(self.graphTypeBox)
        self.graphTypeComboBox.show()
        self.graphTypeLabel.show()
        self.graphTypeBox.show()
        
        
        self.dataParserButton = gtk.Button("Manipulate Data Files")
        self.dataParserButton.connect("clicked", self.hello, None) #   <---Open Data Parser()
        self.dataParserButtonBox = gtk.HBox()
        self.dataParserButtonBox.add(self.dataParserButton)
        self.baseVBox2.add(self.dataParserButtonBox)
        self.dataParserButton.show()
        self.dataParserButtonBox.show()
        
        self.parseSettingsBaseBox = gtk.HBox()
        
        self.showRangeToggle = gtk.CheckButton("Show Range?")
        self.showRangeToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.add(self.showRangeToggle)
        self.showRangeToggle.show()
        
        self.showApproximationToggle = gtk.CheckButton("Show Approximation?")
        self.showApproximationToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.add(self.showApproximationToggle)
        self.showApproximationToggle.show()
        
        self.showSDToggle = gtk.CheckButton("Show Standard Deviation?")
        self.showSDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.add(self.showSDToggle)
        self.showSDToggle.show()
        
        self.showGDToggle = gtk.CheckButton("Show Genetic Diversity?")
        self.showGDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.add(self.showGDToggle)
        self.showGDToggle.show()
        
        self.showPDToggle = gtk.CheckButton("Show Phenotypic Diversity?")
        self.showPDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.add(self.showPDToggle)
        self.showPDToggle.show()
        
        self.compareGDPDToggle = gtk.CheckButton("Compare G.D. and P.D.?")
        self.compareGDPDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.add(self.compareGDPDToggle)
        self.compareGDPDToggle.show()
        
        self.showBestToggle = gtk.CheckButton("Show Best Values?")
        self.showBestToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.add(self.showBestToggle)
        self.showBestToggle.show()
        
        self.showAverageToggle = gtk.CheckButton("Show Average?")
        self.showAverageToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.add(self.showAverageToggle)
        self.showAverageToggle.show()
        
        self.baseVBox2.add(self.parseSettingsBaseBox)
        self.parseSettingsBaseBox.show()
        
        
        #self.showRangeToggle = gtk.CheckButton("Show Range?")
        #self.showRangeToggle.connect("toggled", self.hello, None)
        #self.parseSettingsBaseBox.add(self.showRangeToggle)
        
        self.graphItButton = gtk.Button("Graph It!")
        self.graphItButton.connect("clicked", self.hello, None) #   <---Run Graph It()
        self.graphItButtonBox = gtk.HBox()
        self.graphItButtonBox.add(self.graphItButton)
        self.baseVBox2.add(self.graphItButtonBox)
        self.graphItButton.show()
        self.graphItButtonBox.show()
        
        previousSettings = False
        if(previousSettings == False):
            return False
        else:
            return #loadDefaults
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
