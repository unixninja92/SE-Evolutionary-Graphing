import gtk
import gui_components
import graphsettings

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
        
        self.importedSettings = graphsettings.GraphSettings()
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
        self.baseHBoxForVBox.add(self.baseVBox2)
        self.baseVBox2.show()

        self.titleBox = gui_components.LabelEntryBox("Title")
        self.baseVBox2.pack_start(self.titleBox.getHBox(), False, False, 5)

        self.xTitleBox = gui_components.LabelEntryBox("X-Axis Label")
        self.baseVBox2.pack_start(self.xTitleBox.getHBox(), False, False, 5)

        self.yTitleBox = gui_components.LabelEntryBox("Y-Axis Label")
        self.baseVBox2.pack_start(self.yTitleBox.getHBox(), False, False, 5)
        
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
        self.fontBox.pack_start(self.fontLabel, False, False, 5)
        self.fontBox.pack_start(self.fontComboBox, False, False, 5)
        self.baseVBox2.pack_start(self.fontBox, False, False, 5)
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
        self.fontSizeBox.pack_start(self.fontSizeLabel, False, False, 5)
        self.fontSizeBox.pack_start(self.fontSizeComboBox, False, False, 5)
        self.baseVBox2.pack_start(self.fontSizeBox, False, False, 5)
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
        self.fontColorBox.pack_start(self.fontColorLabel, False, False, 5)
        self.fontColorBox.pack_start(self.fontColorComboBox, False, False, 5)
        self.baseVBox2.pack_start(self.fontColorBox, False, False, 5)
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
        self.graphTypeBox.pack_start(self.graphTypeLabel, False, False, 5)
        self.graphTypeBox.pack_start(self.graphTypeComboBox, False, False, 5)
        self.baseVBox2.pack_start(self.graphTypeBox, False, False, 5)
        self.graphTypeComboBox.show()
        self.graphTypeLabel.show()
        self.graphTypeBox.show()
        
        self.parseSettingsBaseBox = gtk.VBox()
        
        self.showRangeToggle = gtk.CheckButton("Show Range?")
        self.showRangeToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showRangeToggle, False, False, 5)
        self.showRangeToggle.show()
        
        self.showApproximationToggle = gtk.CheckButton("Show Approximation?")
        self.showApproximationToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showApproximationToggle, False, False, 5)
        self.showApproximationToggle.show()
        
        self.showSDToggle = gtk.CheckButton("Show Standard Deviation?")
        self.showSDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showSDToggle, False, False, 5)
        self.showSDToggle.show()
        
        self.showGDToggle = gtk.CheckButton("Show Genetic Diversity?")
        self.showGDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showGDToggle, False, False, 5)
        self.showGDToggle.show()
        
        self.showPDToggle = gtk.CheckButton("Show Phenotypic Diversity?")
        self.showPDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showPDToggle, False, False, 5)
        self.showPDToggle.show()
        
        self.compareGDPDToggle = gtk.CheckButton("Compare G.D. and P.D.?")
        self.compareGDPDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.compareGDPDToggle, False, False, 5)
        self.compareGDPDToggle.show()
        
        self.showBestToggle = gtk.CheckButton("Show Best Values?")
        self.showBestToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showBestToggle, False, False, 5)
        self.showBestToggle.show()
        
        self.showAverageToggle = gtk.CheckButton("Show Average?")
        self.showAverageToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showAverageToggle, False, False, 5)
        self.showAverageToggle.show()
        
        self.baseVBox.add(self.parseSettingsBaseBox)
        self.parseSettingsBaseBox.show()
        
        
        self.dataParserButton = gtk.Button("Manipulate Data Files")
        self.dataParserButton.connect("clicked", self.hello, None) #   <---Open Data Parser()
        self.dataParserButtonBox = gtk.HBox()
        self.dataParserButtonBox.pack_start(self.dataParserButton, False, False, 5)
        self.baseVBox.pack_start(self.dataParserButtonBox, False, False, 5)
        self.dataParserButton.show()
        self.dataParserButtonBox.show()
        
        
        self.graphItButton = gtk.Button("Graph It!")
        self.graphItButton.connect("clicked", self.hello, None) #   <---Run Graph It()
        self.graphItButtonBox = gtk.HBox()
        self.graphItButtonBox.pack_start(self.graphItButton, False, False, 5)
        self.baseVBox2.pack_start(self.graphItButtonBox, False, False, 5)
        self.graphItButton.show()
        self.graphItButtonBox.show()
        
        
        
        #Placeholder for Default Settings Method
        #previousSettings = False
        #if(previousSettings == False):
        #    return False
        #else:
        #    return #loadDefaults
        
        

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
