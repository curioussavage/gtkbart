from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Bartapp/station.ui')
class Station(Gtk.ListBoxRow):
    __gtype_name__ = 'Station'

    station_name = GtkTemplate.Child()
    fav_button = GtkTemplate.Child()
    def __init__(self, station, update_fav, inval_sort, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        self.update_fav_state = update_fav
        self.inval_sort = inval_sort
        self.station = station

        if self.station.is_fav:
            self.fav_button.get_child().set_from_resource('/org/gnome/Bartapp/star.png')

        self.station_name.set_text(station.name)

        self.fav_button.connect('button-press-event', self.on_button_pressed)
        self.fav_button.connect('button-release-event', self.on_button_released)

    def on_realize(self, widget):
        hand_pointer = Gdk.Cursor(Gdk.CursorType.HAND1)
        window = self.get_window()
        window.set_cursor(hand_pointer)

    def on_button_pressed(self, widget, event):
        # this should change the opacity darker to show its pressed (maybe)
        return True

    def inval_sort_cb(self):
        self.inval_sort()

    def on_button_released(self, widget, event):
        if self.update_fav_state(self.station.abbr):
            self.fav_button.get_child().set_from_resource('/org/gnome/Bartapp/star.png')
        else:
            self.fav_button.get_child().set_from_resource('/org/gnome/Bartapp/star-o.png')
        GLib.timeout_add(500, self.inval_sort_cb)
        return True # returning true makes it so the event does not propagate


# class ImageButton(Gtk.EventBox):
#     def __init__(self):
#         super(Gtk.EventBox, self).__init__()

        # Load the images for the button
#         self.button_image = Gtk.Image.new_from_icon_name("edit-delete", Gtk.IconSize.MENU)
#         self.button_pressed_image = Gtk.Image.new_from_icon_name("edit-delete-symbolic", Gtk.IconSize.MENU)

        # Add the default image to the event box
#         self.add(self.button_image)

        # Connect the signal listeners
#         self.connect('realize', self.on_realize)
#         self.connect('button-press-event', self.on_button_pressed)
#         self.connect('button-release-event', self.on_button_released)


#     def update_image(self, image_widget):
#         self.remove(self.get_child())
#         self.add(image_widget)
#         self.button_pressed_image.show()

#     def on_realize(self, widget):
#         hand_pointer = Gdk.Cursor(Gdk.CursorType.HAND1)
#         window = self.get_window()
#         window.set_cursor(hand_pointer)

#     def on_button_pressed(self, widget, event):
#         self.update_image(self.button_pressed_image)

#     def on_button_released(self, widget, event):
#         self.update_image(self.button_image)
