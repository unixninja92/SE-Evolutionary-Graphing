#author: Brendan Linehan
#This program creates the Settings GUI and can open the data parser and grapher based on inputted settings

import gtk
import gui_components
import graphsettings
import sys

class GraphSettingsGUI:
    
    def hello():
        return False

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()
    
    #Function to open graph
    def graphItOpen(self, widget, data=None):
        self.importedSettings.Settings.setConfig(self.titleBox.get_text(), self.fontSizeComboBox.get_active(), self.fontComboBox.get_active(), self.fontColorComboBox.get_active(), self.graphTypeComboBox.get_active(), self.xTitleBox.get_text(), self.yTitleBox.get_text(), self.showApproximationToggle.get_active(), self.showRangeToggle.get_active(), self.showSDToggle.get_active(), False, self.showGDToggle.get_active(), self.showPDToggle.get_active(), self.compareGDPDToggle.get_active(), self.showBestToggle.get_active(), self.showAverageToggle.get_active())
        self.importedSettings.saveSettings()
        self.importedSettings.graph()
        
    def newData(self, widget, data):
        proc = subprocess.Popen(["python parsing_gui.py %s" % self.dataToParse.FileToSave.replace(' ', '\ ')], bufsize=2048, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.window.destroy()

    def __init__(self):
        
        #Lists for combo boxes
        
        fontSizeList = ["10", "12", "14", "16", "18", "20", "22", "24",]
        fontTypeList = ["Arial", "Times New Roman", "Calibri", "Sans Serif", "Comic Sans"]
        fontColorList = ["Blue", "Green", "Red", "Cyan", "Magenta", "Yellow", "Black", "White"]
        graphTypeList = ["Line", "Scatterplot", "Bar", "Pie Chart"]
        
        
        #File from data parser
        self.parseDataLoad = sys.argv[1]
        
        self.importedSettings = graphsettings.GraphSettings(self.parseDataLoad)
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.window.set_position(gtk.WIN_POS_CENTER)
        
        
        #Creates outline for GUI widgets        
        self.baseHBoxForVBox = gtk.HBox()
        self.window.add(self.baseHBoxForVBox)
        self.baseHBoxForVBox.show()
        self.baseVBox = gtk.VBox()
        self.baseHBoxForVBox.pack_start(self.baseVBox, False, False, 5)
        self.baseVBox.show()
        self.baseVBox2 = gtk.VBox()
        self.baseHBoxForVBox.pack_start(self.baseVBox2, False, False, 5)
        self.baseVBox2.show()
        
        #Creates text entry box for title
        self.titleBox = gui_components.LabelEntryBox("Title")
        self.titleBox.set_text(self.importedSettings.Settings.title)
        self.baseVBox2.pack_start(self.titleBox.getHBox(), False, False, 5)
        

        #Creates text entry box for x-axis
        self.xTitleBox = gui_components.LabelEntryBox("X-Axis Label")
        self.xTitleBox.set_text(self.importedSettings.Settings.xAxis)
        self.baseVBox2.pack_start(self.xTitleBox.getHBox(), False, False, 5)


        #Creates text entry box for title
        self.yTitleBox = gui_components.LabelEntryBox("Y-Axis Label")
        self.yTitleBox.set_text(self.importedSettings.Settings.yAxis)
        self.baseVBox2.pack_start(self.yTitleBox.getHBox(), False, False, 5)
        
        
        #Creates combo box for font type 
        self.fontComboBox = gtk.combo_box_new_text()
        for x in range(0, 5):
            i = x
            j = x
            self.fontComboBox.insert_text(j, fontTypeList[i])
        self.fontComboBox.set_active(self.importedSettings.Settings.fontType)
        self.fontComboBoxEntry = self.fontComboBox.get_active_text()
        self.fontLabel = gtk.Label("Font")
        self.fontBox = gtk.HBox()
        self.fontBox.pack_start(self.fontLabel, False, False, 5)
        self.fontBox.pack_start(self.fontComboBox, False, False, 5)
        self.baseVBox2.pack_start(self.fontBox, False, False, 5)
        self.fontComboBox.show()
        self.fontLabel.show()
        self.fontBox.show()
        
        
        #Creates combo box for font size
        self.fontSizeComboBox = gtk.combo_box_new_text()
        for x in range(0, 8):
            i = x
            j = x
            self.fontSizeComboBox.insert_text(j, fontSizeList[i])
        self.fontSizeComboBox.set_active(self.importedSettings.Settings.size)
        self.fontSizeComboBoxEntry = self.fontSizeComboBox.get_active_text()
        self.fontSizeLabel = gtk.Label("Font Size")
        self.fontSizeBox = gtk.HBox()
        self.fontSizeBox.pack_start(self.fontSizeLabel, False, False, 5)
        self.fontSizeBox.pack_start(self.fontSizeComboBox, False, False, 5)
        self.baseVBox2.pack_start(self.fontSizeBox, False, False, 5)
        self.fontSizeComboBox.show()
        self.fontSizeLabel.show()
        self.fontSizeBox.show()
        
        #Creates combo box for font color
        self.fontColorComboBox = gtk.combo_box_new_text()
        for x in range(0, len(fontColorList)):
            i = x
            j = x
            self.fontColorComboBox.insert_text(j, fontColorList[i])
        self.fontColorComboBox.set_active(self.importedSettings.Settings.color)
        self.fontColorComboBoxEntry = self.fontColorComboBox.get_active_text()
        self.fontColorLabel = gtk.Label("Font Color")
        self.fontColorBox = gtk.HBox()
        self.fontColorBox.pack_start(self.fontColorLabel, False, False, 5)
        self.fontColorBox.pack_start(self.fontColorComboBox, False, False, 5)
        self.baseVBox2.pack_start(self.fontColorBox, False, False, 5)
        self.fontColorComboBox.show()
        self.fontColorLabel.show()
        self.fontColorBox.show()
        
        #Creates combo box for graph type and stores entry
        self.graphTypeComboBox = gtk.combo_box_new_text()
        for x in range(0, 4):
            i = x
            j = x
            self.graphTypeComboBox.insert_text(j, graphTypeList[i])
        self.graphTypeComboBox.set_active(self.importedSettings.Settings.graphType)
        self.graphTypeComboBoxEntry = self.graphTypeComboBox.get_active_text()
        self.graphTypeLabel = gtk.Label("Graph Type")
        self.graphTypeBox = gtk.HBox()
        self.graphTypeBox.pack_start(self.graphTypeLabel, False, False, 5)
        self.graphTypeBox.pack_start(self.graphTypeComboBox, False, False, 5)
        self.baseVBox2.pack_start(self.graphTypeBox, False, False, 5)
        self.graphTypeComboBox.show()
        self.graphTypeLabel.show()
        self.graphTypeBox.show()
        
        
        #Creates holder box for toggle settings
        self.parseSettingsBaseBox = gtk.VBox()
        
        #Creates check box for range and gets entry
        self.showRangeToggle = gtk.CheckButton("Show Range?")
        self.showRangeToggle.set_active(self.importedSettings.Settings.ploteRanges)
        self.showRangeToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showRangeToggle, False, False, 5)
        self.showRangeToggle.show()
        
        #Creates check box for show approximation and gets entry
        self.showApproximationToggle = gtk.CheckButton("Show Approximation?")
        self.showApproximationToggle.set_active(self.importedSettings.Settings.approximation)
        self.showApproximationToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showApproximationToggle, False, False, 5)
        self.showApproximationToggle.show()
        
        #Creates check box fo show standard deviation and gets entry
        self.showSDToggle = gtk.CheckButton("Show Standard Deviation?")
        self.showSDToggle.set_active(self.importedSettings.Settings.plotStandDev)
        self.showSDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showSDToggle, False, False, 5)
        self.showSDToggle.show()
        
        #Creates check box for show genetic diversity and gets entry
        self.showGDToggle = gtk.CheckButton("Show Genetic Diversity?")
        self.showGDToggle.set_active(self.importedSettings.Settings.plotGenDiversity)
        self.showGDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showGDToggle, False, False, 5)
        self.showGDToggle.show()
        
        #Creates check box for show phenotype diversity and gets entry
        self.showPDToggle = gtk.CheckButton("Show Phenotypic Diversity?")
        self.showPDToggle.set_active(self.importedSettings.Settings.plotPhenodiversity)
        self.showPDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showPDToggle, False, False, 5)
        self.showPDToggle.show()
        
        #Creates check box for comparing genetic and phenotypic diversity and gets entry
        self.compareGDPDToggle = gtk.CheckButton("Compare G.D. and P.D.?")
        self.compareGDPDToggle.set_active(self.importedSettings.Settings.comparegp)
        self.compareGDPDToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.compareGDPDToggle, False, False, 5)
        self.compareGDPDToggle.show()
        
        #Creates check box for show best values and gets entry
        self.showBestToggle = gtk.CheckButton("Show Best Values?")
        self.showBestToggle.set_active(self.importedSettings.Settings.plotBestVals)
        self.showBestToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showBestToggle, False, False, 5)
        self.showBestToggle.show()
        
        #Creates check box for show average and gets entry
        self.showAverageToggle = gtk.CheckButton("Show Average?")
        self.showAverageToggle.set_active(self.importedSettings.Settings.plotAverages)
        self.showAverageToggle.connect("toggled", self.hello, None)
        self.parseSettingsBaseBox.pack_start(self.showAverageToggle, False, False, 5)
        self.showAverageToggle.show()
        
        #Adds the checkboxes and holder for the checkbox to main holder
        self.baseVBox.pack_start(self.parseSettingsBaseBox, False, False, 5)
        self.parseSettingsBaseBox.show()
        
        #Creates button to open data parser
        self.dataParserButton = gtk.Button("Manipulate Data Files")
        self.dataParserButton.connect("clicked", self.hello, None) #   <---Open Data Parser()
        self.dataParserButtonBox = gtk.HBox()
        self.dataParserButtonBox.pack_start(self.dataParserButton, False, False, 5)
        self.baseVBox.pack_start(self.dataParserButtonBox, False, False, 5)
        self.dataParserButton.show()
        self.dataParserButtonBox.show()
        
        #Creates button to graph it
        self.graphItButton = gtk.Button("Graph It!")
        self.graphItButton.connect("clicked", self.graphItOpen, None) #   <---Run Graph It()
        self.graphItButtonBox = gtk.HBox()
        self.graphItButtonBox.pack_start(self.graphItButton, False, False, 5)
        self.baseVBox2.pack_start(self.graphItButtonBox, False, False, 5)
        self.graphItButton.show()
        self.graphItButtonBox.show()

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
