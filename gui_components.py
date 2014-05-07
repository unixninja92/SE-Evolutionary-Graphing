import gtk

class LabelEntryBox:
    def __init__(self, l):
        self.hbox = gtk.HBox()
        self.label = gtk.Label(l)
        self.entry = gtk.Entry()
        
        self.hbox.set_spacing(3)

        self.hbox.pack_start(self.label, False, False, 0)
        self.hbox.pack_start(self.entry, False, False, 0)

        self.label.show()
        self.entry.show()
        self.hbox.show()

    def getHBox(self):
        return self.hbox

    def getEntry(self):
        return self.entry.get_text()

    def get_text(self):
        return self.entry.get_text()

    def set_text(self, text):
        self.entry.set_text(text)

    def set_width_chars(self, nChars):
        self.entry.set_width_chars(nChars)

    def set_sensitive(self, sensitive):
        self.label.set_sensitive(sensitive)
        self.entry.set_sensitive(sensitive)

class LabelNumBox(LabelEntryBox):
    def __init__(self, l, w):
        LabelEntryBox.__init__(self, l)
        self.entry.destroy()
        self.entry = NumericEntry()
        self.set_width_chars(w)
        self.hbox.add(self.entry)
        self.entry.show()


class NumericEntry(gtk.Entry):
    def __init__(self):
        gtk.Entry.__init__(self)
        self.connect('changed', self.on_changed)

    def on_changed(self, *args):
        text = self.get_text().strip()
        self.set_text(''.join([i for i in text if i in '0123456789']))