import gtk

sets = []


class DataParsingGUI:
    numSets = -1
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
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
        self.scrollSets.set_size_request(400,250)
        self.scrollSets.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_NEVER)
        self.baseVBox.pack_start(self.scrollSets, True, True, 0)
        self.scrollSets.show()

        self.setHBox = gtk.HBox()
        self.scrollSets.add_with_viewport(self.setHBox)
        self.setHBox.show()

        self.boxsets = []

        self.setInteraction = gtk.HBox()
        self.baseVBox.pack_start(self.setInteraction, False, False, 1)
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

        self.parseDataButton = gtk.Button("Parse Data")
        self.setInteraction.pack_start(self.parseDataButton, True, False, 1)
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
        #elif respons == gtk.RESPONSE_CANCEL:
        fileSelect.destroy()
        
        #have thing for both data that needs to be parsed and 
    def newRun(self, widget, data):
        self.addButton.set_sensitive(False)
        self.numSets += 1 
        sets.append([])
        self.boxsets.append(setBox(self.numSets, self.setHBox, self.boxsets, sets[self.numSets]))
#        self.box.addToWindow(self.setHBox)
        # self.box.show()

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

        self.setVBox.add(self.setList)

        self.setBottonBox = gtk.HBox()
        self.setVBox.pack_start(self.setBottonBox, False, False, 0)

        self.addButton = gtk.Button("+")
        self.addButton.connect("clicked", self.addFiles, 1)
        self.setBottonBox.pack_start(self.addButton, False, False, 0)
        self.addButton.show()

        self.removeButton = gtk.Button("-")
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

    def destroy(self, widget, data):
        # self.setFrame.hide()
        # del self.boxsets[self.boxsets.index(self)]
        del self.fileList[:]
        self.setFrame.destroy()
        

if __name__ == "__main__":
    hello = DataParsingGUI()
    hello.main()
