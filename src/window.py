# window.py
#
# Copyright 2019 curioussavage
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import requests

from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
from .gi_composites import GtkTemplate

from .stations import STATIONS
from .station import Station as StationWidget


class Station(GObject.GObject):
    def __init__(self, station_dict):
        GObject.GObject.__init__(self)
        self.name = station_dict.get('name')
        self.abbr = station_dict.get('abbr')


api_key='MW9S-E7SL-26DU-VV8V'
estimate_url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={station}&key={api_key}&json=y'


@GtkTemplate(ui='/org/gnome/Bartapp/window.ui')
class BartappWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'BartappWindow'

    back_button = GtkTemplate.Child()
    stack = GtkTemplate.Child()
    station_list = GtkTemplate.Child()
    train_list = GtkTemplate.Child()
    
    station_window = GtkTemplate.Child()
    train_window = GtkTemplate.Child()
    
    station_list_store = Gio.ListStore()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        
        self.station_list.bind_model(self.station_list_store, self.make_station_widget)
        self.station_list.connect('row_activated', self.handle_station_activated)
        
        for station_dict in STATIONS:
            self.station_list_store.append(Station(station_dict))
            
        self.back_button.connect('clicked', self.handle_back_btn_activate)

    def handle_back_btn_activate(self, el):
        self.stack.set_visible_child(self.station_window)
        # maye clear the data from the line page here

    def get_line_estimates(self, station):
        url = estimate_url.format(api_key=api_key, station=station)
        r = requests.get(ur)
        response = r.json()


    def make_station_widget(self, data):
        return StationWidget(data) 
    
    def handle_station_activated(self, container, widget):
        abbr = widget.station.abbr 
        # request data
        self.stack.set_visible_child(self.train_window)
        self.back_button.show()
 
