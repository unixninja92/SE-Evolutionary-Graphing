import gtk
import data_parser
import gui_components

sets = []

#compute gnetic difference and/or phenotipic difference
#if L-systems (only for gentic)
#   - num terminals
#   - num non-terminals
#   - expansion rate
#ask for filname (autogen one first)
#ask for first generation(index) to use


#Finds:
#   -bests 
#   -averages
#   -XValues
#   -deversities 
#   -gnetic diversity 
#   -phenotipic diversity 


class DataParsingGUI:
    numSets = -1
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.dataToParse = data_parser.DataParser()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.window.set_default_size(800, 600)
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.baseVBox = gtk.VBox()
        self.window.add(self.baseVBox)
        self.baseVBox.show()

        self.scrollSets = gtk.ScrolledWindow()
        # self.scrollSets.set_size_request(800,250)
        self.scrollSets.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_NEVER)
        self.baseVBox.pack_start(self.scrollSets, True, True, 3)
        self.scrollSets.show()

        self.setHBox = gtk.HBox()
        self.scrollSets.add_with_viewport(self.setHBox)
        self.setHBox.show()

        self.emptyLabel = gtk.Label("No Data Sets Added")
        self.setHBox.add(self.emptyLabel)
        self.emptyLabel.show()
        self.empty = True

        self.boxsets = []

        #Add pre-parsed data file or add data sets

        self.setInteraction = gtk.HBox()
        self.baseVBox.pack_start(self.setInteraction, False, False, 5)
        self.setInteraction.show()

        self.parsedFrame = gtk.Frame("Parsed Data File")
        self.parsedFrame.set_shadow_type(gtk.SHADOW_OUT)
        self.parsedFrame.show()

        self.parsedLabel = gtk.Label("None")
        self.parsedFrame.add(self.parsedLabel)
        self.parsedLabel.show()
        self.setInteraction.pack_start(self.parsedFrame, True, True, 1)

        self.addButton = gtk.Button("Add Parsed Data File")
        self.addButton.connect("clicked", self.addFile, None)
        self.setInteraction.pack_start(self.addButton, True, False, 1)
        self.addButton.show()

        self.newSetButton = gtk.Button("Add Data Set")
        self.newSetButton.connect("clicked", self.newRun, None)
        self.setInteraction.pack_start(self.newSetButton, True, False, 1)
        self.newSetButton.show()

        #Information about parsed data file that will be created when parse data is pressed

        self.extractBox1 = gtk.HBox()
        self.baseVBox.pack_start(self.extractBox1, False, False, 5)
        self.extractBox1.show()

        self.parsedFileLabel = gtk.Label("Staring Generation:")
        self.extractBox1.pack_start(self.parsedFileLabel, False, False, 1)
        self.parsedFileLabel.show()

        self.startGenEntry = gui_components.NumericEntry()
        self.startGenEntry.set_max_length(3)
        self.startGenEntry.set_width_chars(3)
        self.startGenEntry.set_text("1")
        self.extractBox1.pack_start(self.startGenEntry, False, False, 1)
        self.startGenEntry.show()

        self.geneticDiff = gtk.CheckButton("Compute Genetic Differences")
        self.geneticDiff.connect("toggled", self.isGenetic, None)
        self.extractBox1.pack_start(self.geneticDiff, True, False, 0)
        self.geneticDiff.show()

        self.phenotypicDiff = gtk.CheckButton("Compute Phenotypic Differences")
        self.extractBox1.pack_start(self.phenotypicDiff, True, False, 0)
        self.phenotypicDiff.show()

        self.parsedFileLabel = gtk.Label("File Name:")
        self.extractBox1.pack_start(self.parsedFileLabel, False, False, 1)
        self.parsedFileLabel.show()

        self.parsedFileEntry = gtk.Entry()
        self.extractBox1.pack_start(self.parsedFileEntry, False, False, 1)
        self.parsedFileEntry.show()

        #More info about new data file

        self.extractBox2 = gtk.HBox()
        self.baseVBox.pack_start(self.extractBox2, False, False, 5)
        self.extractBox2.show()

        self.lSystem = gtk.CheckButton("Is an L-System")
        self.lSystem.connect("toggled", self.isLSystem, None)
        self.lSystem.set_sensitive(False)
        self.extractBox2.pack_start(self.lSystem, True, False, 2)
        self.lSystem.show()

        self.terminalLabel = gtk.Label("Number of Terminals:")
        self.terminalLabel.set_sensitive(False)
        self.extractBox2.pack_start(self.terminalLabel, False, False, 1)
        self.terminalLabel.show()

        self.terminalEntry = gui_components.NumericEntry()
        self.terminalEntry.set_width_chars(4)
        self.terminalEntry.set_sensitive(False)
        self.extractBox2.pack_start(self.terminalEntry, False, False, 0)
        self.terminalEntry.show()

        self.nonterminalLabel = gtk.Label("Number of Non-Terminals:")
        self.nonterminalLabel.set_sensitive(False)
        self.extractBox2.pack_start(self.nonterminalLabel, False, False, 1)
        self.nonterminalLabel.show()

        self.nonterminalEntry = gui_components.NumericEntry()
        self.nonterminalEntry.set_width_chars(4)
        self.nonterminalEntry.set_sensitive(False)
        self.extractBox2.pack_start(self.nonterminalEntry, False, False, 0)
        self.nonterminalEntry.show()

        self.expansionLabel = gtk.Label("Expansion Rate:")
        self.expansionLabel.set_sensitive(False)
        self.extractBox2.pack_start(self.expansionLabel, False, False, 1)
        self.expansionLabel.show()

        self.expansionEntry = gui_components.NumericEntry()
        self.expansionEntry.set_width_chars(4)
        self.expansionEntry.set_sensitive(False)
        self.extractBox2.pack_start(self.expansionEntry, False, False, 0)
        self.expansionEntry.show()

        self.parseDataButton = gtk.Button("Parse Data")
        self.extractBox2.pack_end(self.parseDataButton, False, True, 1)
        self.parseDataButton.show()

        self.window.show()

    def addFile(self, widget, data):
        fileSelect = gtk.FileChooserDialog(title = "", action = gtk.FILE_CHOOSER_ACTION_OPEN, buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        self.numSets += 1
        sets.append([])
        response = fileSelect.run()
        if response == gtk.RESPONSE_OK:
            sets[self.numSets].append(fileSelect.get_filename())
            self.parsedLabel.set_text(fileSelect.get_filename())
            self.addButton.set_sensitive(False)
            self.dataToParse.importPreviousRun(fileSelect.get_filename())
            self.startGenEntry.set_text(self.dataToParse.StartingGeneration)
            self.phenotypicDiff.set_active(self.dataToParse.PhenotypicDifference)
        #elif respons == gtk.RESPONSE_CANCEL:
        fileSelect.destroy()
        
        #have thing for both data that needs to be parsed and 
    def newRun(self, widget, data):
        if self.empty:
            self.emptyLabel.hide()
            self.empty = False
        self.addButton.set_sensitive(False)
        self.numSets += 1 
        sets.append([])
        self.boxsets.append(setBox(self.numSets, self.setHBox, self.boxsets, sets[self.numSets]))
#        self.box.addToWindow(self.setHBox)
        # self.box.show()

    def parseData(self, widget, data):
        self.dataToParse.setConfig(sets, self.parsedFileEntry.get_text(), ".", self.startGenEntry.get_text(), self.geneticDiff.get_active(), self.phenotypicDiff.get_active())
        # this.dataToParse.parseData()

    def isGenetic(self, widget, data):
        self.lSystem.set_sensitive(not self.lSystem.get_sensitive())

    def isLSystem(self, widget, data):
        boolean = not self.terminalLabel.get_sensitive()
        self.terminalLabel.set_sensitive(boolean)
        self.terminalEntry.set_sensitive(boolean)
        self.nonterminalEntry.set_sensitive(boolean)
        self.nonterminalLabel.set_sensitive(boolean)
        self.expansionLabel.set_sensitive(boolean)
        self.expansionEntry.set_sensitive(boolean)

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

class setBox:
    def __init__(self, setNum, box, boxsets, data):
        self.boxsets = boxsets
        self.numSet = setNum
        self.fileList = data

        self.setFrame = gtk.Frame()
        self.setFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)

        self.setVBox = gtk.VBox()
        self.setFrame.add(self.setVBox)

        self.setTopBox = gtk.HBox()
        self.setVBox.pack_start(self.setTopBox, False, False, 0)




        self.setLabel = gtk.Label('Data Set %i' % self.numSet)
        self.setTopBox.pack_start(self.setLabel, True, True, 1)
        self.setLabel.show()

        self.closeButton = gtk.Button("x")
        self.closeButton.connect("clicked", self.destroy, None)
        self.setTopBox.pack_start(self.closeButton, False, False, 1)
        self.closeButton.show()


        self.scrollSets = gtk.ScrolledWindow()
        self.scrollSets.set_size_request(375,250)
        self.scrollSets.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.setVBox.pack_start(self.scrollSets, True, True, 0)
        self.scrollSets.show()

        self.treestore = gtk.TreeStore(str)
        # for parent in range(8):
            # piter = self.treestore.append(None, ['parent %i' % parent])
            # for child in range(3):
            #     self.treestore.append(piter, ['child %i of parent %i' %(child, parent)])

        self.setList = gtk.TreeView(self.treestore)

        

        self.fileCol = gtk.TreeViewColumn("Folders")
        self.fileCol.Title = "Run " + str(self.numSet)

        self.fileCell = gtk.CellRendererText()
        self.fileCol.pack_start(self.fileCell, True)

        self.fileIter = self.setList.append_column(self.fileCol)
        self.fileCol.add_attribute(self.fileCell, "text", 0)

        print("new set!!")

        self.scrollSets.add(self.setList)

        self.setBottonBox = gtk.HBox()
        self.setVBox.pack_start(self.setBottonBox, False, False, 0)

        self.addButton = gtk.Button("+")
        self.addButton.connect("clicked", self.addFiles, 1)
        self.setBottonBox.pack_start(self.addButton, False, False, 0)
        self.addButton.show()

        self.removeButton = gtk.Button("-")
        self.removeButton.connect("clicked", self.removeFiles, None)
        self.setBottonBox.pack_start(self.removeButton, False, False, 0)
        self.removeButton.show()

        box.pack_start(self.setFrame, True, True, 0)

        self.setList.show()
        self.setVBox.show()
        self.setTopBox.show()
        self.setBottonBox.show()
        self.setFrame.show()
        

    def addFiles(self, widget, data):
        fileSelect = gtk.FileChooserDialog(title = "", action = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        fileSelect.set_select_multiple(True)
        
        response = fileSelect.run()
        if response == gtk.RESPONSE_OK:
            # print(fileSelect.get_filenames())
            # sets[numSet].append(fileSelect.get_filenames())
            for f in fileSelect.get_filenames():
                self.fileList.append(f)
                # sets[self.numSet].append(f)
                self.treestore.append(None, [f])
        #elif respons == gtk.RESPONSE_CANCEL:
        fileSelect.destroy()
        print(sets)

    def removeFiles(self, widget, data):
        tree_selection = self.setList.get_selection()
        (model, pathlist) = tree_selection.get_selected_rows()
        tree_iter = model.get_iter(pathlist[0])
        filePath = model.get_value(tree_iter,0)
        self.treestore.remove(tree_iter)
        del self.fileList[self.fileList.index(filePath)]
        print("remove")
        print(filePath)

    def destroy(self, widget, data):
        # self.setFrame.hide()
        # del self.boxsets[self.boxsets.index(self)]
        del self.fileList[:]
        self.setFrame.destroy()
        



if __name__ == "__main__":
    hello = DataParsingGUI()
    hello.main()
