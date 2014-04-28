import gtk

runs = []


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
        self.window.set_size_request(400, 300)

        self.baseVBox = gtk.VBox()
        self.window.add(self.baseVBox)
        self.baseVBox.show()

        self.scrollRun = gtk.ScrolledWindow()
        self.scrollRun.set_size_request(400,250)
        self.scrollRun.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_AUTOMATIC)
        self.baseVBox.add(self.scrollRun)
        self.scrollRun.show()

        self.runHBox = gtk.HBox()
        self.scrollRun.add_with_viewport(self.runHBox)
        self.runHBox.show()

        self.runInteraction = gtk.HBox()
        self.baseVBox.add(self.runInteraction)
        self.runInteraction.show()

        self.newRunButton = gtk.Button("Add Run")
        self.newRunButton.connect("clicked", self.newRun, None)
        self.runInteraction.add(self.newRunButton)
        self.newRunButton.show()

        self.addButton = gtk.Button("Add File")
        self.addButton.connect("clicked", self.addFiles, 1)
        self.runInteraction.add(self.addButton)
        self.addButton.show()

        self.window.show()

    def addFiles(self, widget, runNum):
        self.fileSelect = gtk.FileChooserDialog(title = "", action = gtk.FILE_CHOOSER_ACTION_OPEN, buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        self.fileSelect.set_select_multiple(True)
        
        self.files = self.fileSelect.run()
        runs[runNum].append(self.fileSelect.get_filenames())
        self.fileSelect.destroy()
        
    def newRun(self, widget, data):
        runs.append([])
        self.runNum = len(runs)-1
        self.box = runBox(self.runNum, self.runHBox)
#        self.box.addToWindow(self.runHBox)
#        self.box.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

class runBox:
    def __init__(self, run, box):
        self.treestore = gtk.TreeStore(str)
        for parent in range(4):
            piter = self.treestore.append(None, ['parent %i' % parent])
            for child in range(3):
                self.treestore.append(piter, ['child %i of parent %i' %(child, parent)])

        self.runList = gtk.TreeView(self.treestore)
        box.add(self.runList)
        

        self.fileCol = gtk.TreeViewColumn()
        self.fileCol.Title = "Run " + str(run)

        self.fileCell = gtk.CellRendererText()
        self.fileCol.pack_start(self.fileCell, True)

        self.runList.append_column(self.fileCol)
        self.fileCol.add_attribute(self.fileCell, "text", 0)

        print("new run!!")

        self.runList.show()
        
    def show(self):
        self.runList.show()

    def addToWindow(self, window):
        window.add(self.runList)
        

if __name__ == "__main__":
    hello = DataParsingGUI()
    hello.main()
