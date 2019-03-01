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
from .line import Line as LineWidget
from .platform_divider import PlatformDivider


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


api_key='QPMZ-5J67-9D4T-DWE9'
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
    train_list_store = Gio.ListStore()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('window init')
        self.init_template()
        
        self.station_list.bind_model(self.station_list_store, self.make_station_widget)
        self.station_list.connect('row_activated', self.handle_station_activated)
        
        self.train_list.bind_model(self.train_list_store, self.make_train_widget)

        for station_dict in STATIONS:
            self.station_list_store.append(Station(station_dict))
            
        self.back_button.connect('clicked', self.handle_back_btn_activate)

    def make_train_widget(self, data):
        if hasattr(data, 'number'):
            return PlatformDivider(data.number)
        return LineWidget(data)

    def handle_back_btn_activate(self, el):
        self.stack.set_visible_child(self.station_window)
        # maye clear the data from the line page here
        self.back_button.visibile = False
        self.train_list_store.remove_all()
        print('back button clicked')

    def get_line_estimates(self, station):
        url = estimate_url.format(api_key=api_key, station=station)
        headers = {
            'User-Agent': 'gtkbart',
        }
        try:
            r = requests.get(url, headers=headers)
            response = r.json().get('root')


            # .get('station')[0].get('etd') is the actual dict of data
            etd = response.get('station')[0].get('etd')
            print('etd')
            print(etd)
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

            for pnum, lines in platforms.items():
                self.train_list_store.append(Divider(pnum))
                print('adding platform')
                for _, line in lines.items():
                    print('adding line')
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
 
