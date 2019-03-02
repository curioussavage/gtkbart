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
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from .gi_composites import GtkTemplate

from .stations import STATIONS
from .station import Station as StationWidget
from .line import Line as LineWidget
from .platform_divider import PlatformDivider
from .station_header import StationHeader as StationHeaderWidget


class Station(GObject.GObject):
    def __init__(self, station_dict):
        GObject.GObject.__init__(self)
        self.name = station_dict.get('name')
        self.abbr = station_dict.get('abbr')


class Divider(GObject.GObject):
     def __init__(self, number):
        GObject.GObject.__init__(self)
        self.number = number


class Line(GObject.GObject):
    def __init__(self, name, abbrev, estimate):
        GObject.GObject.__init__(self)
        self.name = name
        self.abbr = abbrev
        self.times = [estimate.get('minutes')]
        self.cars = estimate.get('length')


class StationHeader(GObject.GObject):
     def __init__(self, name):
        GObject.GObject.__init__(self)
        self.name = name


api_key='QPMZ-5J67-9D4T-DWE9'
estimate_url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={station}&key={api_key}&json=y'

# style_provider = Gtk.CssProvider()

# css = b"""
# GtkButton {
#     border-color: #000;
#     background-color: #000;
# }
# """

# style_provider.load_from_data(css)

# Gtk.StyleContext.add_provider_for_screen(
#     Gdk.Screen.get_default(),
#     style_provider,
#     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
# )

@GtkTemplate(ui='/org/gnome/Bartapp/window.ui')
class BartappWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'BartappWindow'

    back_button = GtkTemplate.Child()
    stack = GtkTemplate.Child()
    station_list = GtkTemplate.Child()
    train_list = GtkTemplate.Child()
    
    station_window = GtkTemplate.Child()
    train_window = GtkTemplate.Child()
    
    train_list_store = Gio.ListStore()
    
    station_filter_search = GtkTemplate.Child()
    current_filter = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('window init')
        self.init_template()
        
        self.train_list.bind_model(self.train_list_store, self.make_train_widget)

        self.station_list.connect('row_activated', self.handle_station_activated)
        self.station_list.set_filter_func(self.filter_station_list, None, False)
        for station_dict in STATIONS:
            self.station_list.add(self.make_station_widget(Station(station_dict)))
        self.station_list.show_all()
            
        self.back_button.connect('clicked', self.handle_back_btn_activate)
        self.station_filter_search.connect('search-changed', self.update_filter)

    def update_filter(self, search_input):
        self.current_filter = search_input.get_text()
        self.station_list.invalidate_filter()

    def filter_station_list(self, row, data, notify_destroy):
        name = row.station.name
        if self.current_filter:
            return self.current_filter.lower() in row.station.name.lower()
        else:
            return True

    def make_train_widget(self, data):
        if isinstance(data, Divider):
            return PlatformDivider(data.number)
        if isinstance(data, StationHeader):
            return StationHeaderWidget(data.name)
        if isinstance(data, Line):
            return LineWidget(data)
        raise Exception('Could not find widget for data class')

    def handle_back_btn_activate(self, el):
        self.stack.set_visible_child(self.station_window)
        self.back_button.visibile = False
        self.train_list_store.remove_all()

    def get_line_estimates(self, station):
        url = estimate_url.format(api_key=api_key, station=station)
        headers = {
            'User-Agent': 'gtkbart',
        }
        try:
            r = requests.get(url, headers=headers)
            response = r.json().get('root')

            etd = response.get('station')[0].get('etd')
            platforms = {}
            for dest in etd:
                abbrev = dest.get('abbreviation')
                for estimate in dest.get('estimate'):
                    platform_number = estimate.get('platform')
                    if not platform_number in platforms:
                        platforms[platform_number] = {}
                    if not platforms[platform_number].get(abbrev):
                        platforms[platform_number][abbrev] = Line(dest['destination'], dest['abbreviation'], estimate)
                    else:
                        platforms[platform_number][abbrev].times.append(estimate.get('minutes'))

            self.train_list_store.append(StationHeader(response['station'][0]['name']))
            for pnum, lines in platforms.items():
                self.train_list_store.append(Divider(pnum))
                for _, line in lines.items():
                    self.train_list_store.append(line)

        except Exception as e:
            print(e)


    def make_station_widget(self, data):
        return StationWidget(data) 
    
    def handle_station_activated(self, container, widget):
        abbr = widget.station.abbr 
        # request data
        self.get_line_estimates(abbr)
        self.stack.set_visible_child(self.train_window)
        self.back_button.show()
 
