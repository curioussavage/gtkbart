from gi.repository import Gtk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Bartapp/station_header.ui')
class StationHeader(Gtk.ListBoxRow):
    __gtype_name__ = 'StationHeader'

    station_name = GtkTemplate.Child()
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        markup = '<span size="x-large">{text}</span>'
        self.station_name.set_markup(markup.format(text=name))
        
