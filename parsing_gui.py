import gtk

runs = [[]]


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

        self.baseVBox = gtk.VBox()
        self.window.add(self.baseVBox)
        self.baseVBox.show()

        self.runInteraction = gtk.HBox()
        self.baseVBox.add(self.runInteraction)
        self.runInteraction.show()

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

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

class runBox:
    def __init__(self, run):
        self.base = gtk.HBox()
        self.runName = gtk.Label(run)
        
        self.base.add(self.runName)
        
        self.runName.show()
        self.base.show()

if __name__ == "__main__":
    hello = DataParsingGUI()
    hello.main()


#Have list of currently selected files for each run, and allow user to add folders or files to the list. Then allow user to add more runs.
