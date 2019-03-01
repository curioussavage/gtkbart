from gi.repository import Gtk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Bartapp/line.ui')
class Line(Gtk.ListBoxRow):
    __gtype_name__ = 'Line'

    line_name = GtkTemplate.Child()
    line_detail = GtkTemplate.Child()
    line_time = GtkTemplate.Child()
    def __init__(self, line, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        self.line_name.set_text(line.name)
        self.line_detail.set_text(line.cars + ' car train')
        self.line_time.set_text(', '.join(line.times))
