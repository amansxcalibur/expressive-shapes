import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from bezier_morph_shape import AnimateShapeMorph


class Pill(Gtk.Window):
    def __init__(self):
        super().__init__(title="Pill Window")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.set_type_hint(gi.repository.Gdk.WindowTypeHint.NORMAL)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main_box.set_hexpand(True)
        self.main_box.set_vexpand(True)

        self.morph_widget = AnimateShapeMorph()

        self.main_box.pack_start(self.morph_widget, True, True, 0)
        self.add(self.main_box)

        self.connect("destroy", Gtk.main_quit)


if __name__ == "__main__":
    win = Pill()
    win.show_all()

    Gtk.main()
