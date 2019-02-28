from gi.repository import Gtk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Bartapp/station.ui')
class Station(Gtk.ListBoxRow):
    __gtype_name__ = 'Station'

    station_name = GtkTemplate.Child()
    def __init__(self, station, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        
        self.station_name.set_text(station.name)
        self.station = station
