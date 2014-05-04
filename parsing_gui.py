import gtk

runs = []
# global runNum
runNum = -1


class DataParsingGUI:
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

        self.scrollRun = gtk.ScrolledWindow()
        self.scrollRun.set_size_request(400,250)
        self.scrollRun.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_AUTOMATIC)
        self.baseVBox.pack_start(self.scrollRun, True, True, 0)
        self.scrollRun.show()

        self.runHBox = gtk.HBox()
        self.scrollRun.add_with_viewport(self.runHBox)
        self.runHBox.show()

        self.box = []

        self.runInteraction = gtk.HBox()
        self.baseVBox.pack_start(self.runInteraction, False, False, 1)
        self.runInteraction.show()

        self.parsedFrame = gtk.Frame("Parsed Data File")
        self.parsedFrame.set_shadow_type(gtk.SHADOW_OUT)
        self.runInteraction.pack_start(self.parsedFrame, True, True, 1)
        self.parsedFrame.show()

        self.parsedLabel = gtk.Label("None")
        self.parsedFrame.add(self.parsedLabel)
        self.parsedLabel.show()

        self.addButton = gtk.Button("Add Parsed Data File")
        self.addButton.connect("clicked", self.addFile, None)
        self.runInteraction.pack_start(self.addButton, True, False, 1)
        self.addButton.show()

        self.newRunButton = gtk.Button("Add Data Set")
        self.newRunButton.connect("clicked", self.newRun, None)
        self.runInteraction.pack_start(self.newRunButton, True, False, 1)
        self.newRunButton.show()

        self.window.show()

    def addFile(self, widget, data):
        global runNum
        fileSelect = gtk.FileChooserDialog(title = "", action = gtk.FILE_CHOOSER_ACTION_OPEN, buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        runs.append([])
        runNum += 1
        response = fileSelect.run()
        if response == gtk.RESPONSE_OK:
            runs[runNum].append(fileSelect.get_filename())
            self.parsedLabel.set_text(fileSelect.get_filename())
            self.addButton.set_sensitive(False)
        #elif respons == gtk.RESPONSE_CANCEL:
        fileSelect.destroy()
        
        #have thing for both data that needs to be parsed and 
    def newRun(self, widget, data):
        self.addButton.set_sensitive(False)
        global runNum
        runs.append([])
        runNum += 1
        self.box.append(runBox(self.runHBox))
#        self.box.addToWindow(self.runHBox)
        # self.box.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

class runBox:
    def __init__(self, box):

        self.runFrame = gtk.Frame()
        self.runFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)

        self.runVBox = gtk.VBox()
        self.runFrame.add(self.runVBox)

        self.runHBox = gtk.HBox()
        self.runVBox.pack_start(self.runHBox, False, False, 0)

        self.runLabel = gtk.Label('Data Set %i' % runNum)
        self.runHBox.pack_start(self.runLabel, True, True, 1)
        self.runLabel.show()

        self.addButton = gtk.Button("+")
        self.addButton.connect("clicked", self.addFiles, 1)
        self.runHBox.pack_start(self.addButton, False, False, 0)
        self.addButton.show()

        self.removeButton = gtk.Button("-")
        self.runHBox.pack_start(self.removeButton, False, False, 0)
        self.removeButton.show()

        self.treestore = gtk.TreeStore(str)
        # for parent in range(8):
            # piter = self.treestore.append(None, ['parent %i' % parent])
            # for child in range(3):
            #     self.treestore.append(piter, ['child %i of parent %i' %(child, parent)])

        self.runList = gtk.TreeView(self.treestore)

        

        self.fileCol = gtk.TreeViewColumn()
        self.fileCol.Title = "Run " + str(runNum)

        self.fileCell = gtk.CellRendererText()
        self.fileCol.pack_start(self.fileCell, True)

        self.fileIter = self.runList.append_column(self.fileCol)
        self.fileCol.add_attribute(self.fileCell, "text", 0)

        print("new run!!")

        self.runVBox.add(self.runList)

        box.pack_start(self.runFrame, True, True, 0)

        self.runList.show()
        self.runVBox.show()
        self.runHBox.show()
        self.runFrame.show()
        
    def show(self):
        self.runHBox.show()
        self.runList.show()

    def addToWindow(self, window):
        window.add(self.runHBox)

    def addFiles(self, widget, data):
        fileSelect = gtk.FileChooserDialog(title = "", action = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        fileSelect.set_select_multiple(True)
        
        response = fileSelect.run()
        if response == gtk.RESPONSE_OK:
            # print(fileSelect.get_filenames())
            # runs[runNum].append(fileSelect.get_filenames())
            for f in fileSelect.get_filenames():
                runs[runNum].append(f)
                self.treestore.append(None, [f])
        #elif respons == gtk.RESPONSE_CANCEL:
        fileSelect.destroy()
        print(runs)
        

if __name__ == "__main__":
    hello = DataParsingGUI()
    hello.main()
