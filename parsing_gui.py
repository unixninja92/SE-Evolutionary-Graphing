'''
Evolutionary Graphing
Copyright (C) 2014 Charles Teese

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import gtk
import data_parser
import gui_components
import subprocess

sets = []


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
        self.setInteraction.set_spacing(5)
        self.baseVBox.pack_start(self.setInteraction, False, False, 5)
        self.setInteraction.show()


        self.parsedFrame = gtk.Frame("Parsed Data File")
        self.parsedFrame.set_shadow_type(gtk.SHADOW_OUT)
        self.parsedFrame.show()

        self.parsedLabel = gtk.Label("None")
        self.parsedFrame.add(self.parsedLabel)
        self.parsedLabel.show()
        self.setInteraction.pack_start(self.parsedFrame, False, True, 1)

        self.addButton = gtk.Button("Add Parsed Data File")
        self.addButton.connect("clicked", self.addFile, None)
        self.setInteraction.pack_start(self.addButton, False, False, 1)
        self.addButton.show()

        self.newSetButton = gtk.Button("Add Data Set")
        self.newSetButton.connect("clicked", self.newRun, None)
        self.setInteraction.pack_end(self.newSetButton, False, False, 1)
        self.newSetButton.show()

        #Information about parsed data file that will be created when parse data is pressed

        self.extractBox1 = gtk.HBox()
        self.baseVBox.pack_start(self.extractBox1, False, False, 5)
        self.extractBox1.show()

        self.startGen = gui_components.LabelNumBox("Starting Generation:", 3)
        self.startGen.set_text("1")
        self.extractBox1.pack_start(self.startGen.getHBox(), False, False, 1)

        self.geneticDiff = gtk.CheckButton("Compute Genetic Differences")
        self.geneticDiff.connect("toggled", self.isGenetic, None)
        self.extractBox1.pack_start(self.geneticDiff, True, False, 0)
        self.geneticDiff.show()

        self.phenotypicDiff = gtk.CheckButton("Compute Phenotypic Differences")
        self.extractBox1.pack_start(self.phenotypicDiff, True, False, 0)
        self.phenotypicDiff.show()

        self.parsedFile = gui_components.LabelEntryBox("File Name:")
        self.extractBox1.pack_end(self.parsedFile.getHBox(), False, False, 1)

        #More info about new data file

        self.extractBox2 = gtk.HBox()
        self.baseVBox.pack_start(self.extractBox2, False, False, 5)
        self.extractBox2.show()

        self.lSystem = gtk.CheckButton("Is an L-System")
        self.lSystem.connect("toggled", self.isLSystem, None)
        self.lSystem.set_sensitive(False)
        self.extractBox2.pack_start(self.lSystem, True, False, 2)
        self.lSystem.show()

        self.terminalBox = gui_components.LabelNumBox("Number of Terminals:", 4)
        self.terminalBox.set_sensitive(False)
        self.extractBox2.pack_start(self.terminalBox.getHBox(), True, False, 0)

        self.nonterminalBox = gui_components.LabelNumBox("Number of Non-Terminals:", 4)
        self.nonterminalBox.set_sensitive(False)
        self.extractBox2.pack_start(self.nonterminalBox.getHBox(), True, False, 0)

        self.expansionBox = gui_components.LabelNumBox("Expansion Rate:", 4)
        self.expansionBox.set_sensitive(False)
        self.extractBox2.pack_start(self.expansionBox.getHBox(), True, False, 0)

        self.parseDataButton = gtk.Button("Parse Data")
        self.parseDataButton.connect("clicked", self.parseData, None)
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

            self.startGen.set_text(self.dataToParse.Config.StartingGeneration)
            self.startGen.set_sensitive(False)

            self.phenotypicDiff.set_active(self.dataToParse.Config.PhenotypicDifference)
            self.phenotypicDiff.set_sensitive(False)

            self.geneticDiff.set_active(self.dataToParse.Config.GeneticDifference)
            self.geneticDiff.set_sensitive(False)

            gLSystem = self.dataToParse.Config.GLSystem
            isLSystem = gLSystem[0]

            self.lSystem.set_active(isLSystem)
            self.lSystem.set_sensitive(False)

            if isLSystem:
                self.nonterminalBox.set_text(gLSystem[1])
                self.nonterminalBox.set_sensitive(False)

                self.terminalBox.set_text(gLSystem[2])
                self.terminalBox.set_sensitive(False)

                self.expansionBox.set_text(gLSystem[3])
                self.expansionBox.set_sensitive(False)

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

    def parseData(self, widget, data):
        self.dataToParse.setConfig(sets, self.startGen.get_text(), self.geneticDiff.get_active(), [self.lSystem.get_active(), self.nonterminalBox.get_text(), self.terminalBox.get_text(), self.expansionBox.get_text()], self.phenotypicDiff.get_active())
        progress = ParserProgress()
        self.dataToParse.parseData(progress)
        proc = subprocess.Popen(["python graph_settings_gui.py %s" % self.dataToParse.FileToSave.replace(' ', '\ ')], bufsize=2048, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.window.destroy()

    def isGenetic(self, widget, data):
        sensitive = self.geneticDiff.get_active()
        if not sensitive:
            self.terminalBox.set_sensitive(False)
            self.nonterminalBox.set_sensitive(False)
            self.expansionBox.set_sensitive(False)
        elif self.lSystem.get_active():
            self.terminalBox.set_sensitive(True)
            self.nonterminalBox.set_sensitive(True)
            self.expansionBox.set_sensitive(True)
        self.lSystem.set_sensitive(sensitive)

    def isLSystem(self, widget, data):
        sensitive = self.lSystem.get_active()
        self.terminalBox.set_sensitive(sensitive)
        self.nonterminalBox.set_sensitive(sensitive)
        self.expansionBox.set_sensitive(sensitive)

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

        self.treeStore = gtk.TreeStore(str)

        self.setList = gtk.TreeView(self.treeStore)

        self.folderCol = gtk.TreeViewColumn("Folders")
        self.folderCol.Title = "Run " + str(self.numSet)

        self.folderCell = gtk.CellRendererText()
        self.folderCol.pack_start(self.folderCell, True)

        self.setList.append_column(self.folderCol)
        self.folderCol.add_attribute(self.folderCell, "text", 0)

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
            for f in fileSelect.get_filenames():
                self.fileList.append(f)
                self.treeStore.append(None, [f])
        fileSelect.destroy()
        print(sets)

    def removeFiles(self, widget, data):
        treeSelection = self.setList.get_selection()
        (model, pathlist) = treeSelection.get_selected_rows()
        treeIter = model.get_iter(pathlist[0])
        filePath = model.get_value(treeIter,0)
        self.treeStore.remove(treeIter)
        del self.fileList[self.fileList.index(filePath)]
        print("remove")
        print(filePath)

    def destroy(self, widget, data):
        del self.fileList[:]
        self.setFrame.destroy()
        
class ParserProgress:
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_default_size(200, 100)
        self.window.connect("destroy", lambda w: self.window.hide())
        # self.window.set_decorated(False)

        vbox = gtk.VBox(False, 5)

        self.progressTExt = gtk.Label("Data is being parsed...")
        vbox.pack_start(self.progressTExt)
        self.progressTExt.show()

        self.dirbar = gtk.ProgressBar()
        # vbox.pack_start(self.dirbar)

        self.filebar = gtk.ProgressBar()
        # self.filebar.set_text("1/?")
        # self.filebar.set_fraction(.01)
        # vbox.pack_start(self.filebar)

        self.window.add(vbox)
        self.window.show_all()

    def initFileBar(self, numFiles):
        print("int file bar")
        self.numFiles = numFiles
        self.currentFile = 1
        self.fraction = 1.0/numFiles
        print("fraction: %f" % self.fraction)
        self.filebar.set_text("1/%i" % self.numFiles)
        self.filebar.set_fraction(self.fraction)


    def updateFileBar(self):
        value = self.filebar.get_fraction() + self.fraction
        self.currentFile += 1
        self.filebar.set_text("{0}/{1}".format(self.currentFile, self.numFiles))
        self.filebar.set_fraction(value)

    def destroy(self):
        self.window.destroy()


if __name__ == "__main__":
    hello = DataParsingGUI()
    hello.main()
