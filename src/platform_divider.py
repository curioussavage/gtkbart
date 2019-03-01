from gi.repository import Gtk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/org/gnome/Bartapp/platform_divider.ui')
class PlatformDivider(Gtk.ListBoxRow):
    __gtype_name__ = 'PlatformDivider'

    platform_name = GtkTemplate.Child()
    def __init__(self, number, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        self.platform_name.set_text('Platform ' + number)
