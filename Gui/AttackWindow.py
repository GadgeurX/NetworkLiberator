import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import Packet

class AttackWindow(Gtk.Window):

    def __init__(self, main):
        Gtk.Window.__init__(self, title="Network Liberator")
        self.listbox = Gtk.ListBox()
        self.main = main
        self.set_visible(False)
        self.list_host_store = Gtk.ListStore(str, str, str, str)

        self.list_host_view = Gtk.TreeView(self.list_host_store)

        self.list_host_view.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.list_host_view.get_selection().connect("changed", self.on_tree_selection_changed)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Host Ip/Name", renderer, text=0)
        self.list_host_view.append_column(column)
        column.set_sort_column_id(0)

        column = Gtk.TreeViewColumn("Host Mac", renderer, text=1)
        self.list_host_view.append_column(column)

        column = Gtk.TreeViewColumn("Host Vendor", renderer, text=2)
        self.list_host_view.append_column(column)

        column = Gtk.TreeViewColumn("Host Os", renderer, text=3)
        self.list_host_view.append_column(column)
        

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box_outer)

        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.label_attack = Gtk.Label("Attack the hosts selected", xalign=0)
        hbox.pack_start(self.label_attack, True, True, 0)

        self.switch_attack = Gtk.Switch()
        self.switch_attack.props.valign = Gtk.Align.CENTER
        self.switch_attack.connect("notify::active", self.on_switch_activated)
        hbox.pack_start(self.switch_attack, False, True, 0)

        title = Gtk.Label()
        title.set_markup("<span size='20000'>Network Liberator</span>")

        box_outer.pack_start(title, False, False, 10)
        box_outer.pack_start(hbox, False, False, 0)

        swH = Gtk.ScrolledWindow()
        swH.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        swH.add(self.list_host_view)
        box_outer.pack_start(swH, True, True, 0)

        self.set_default_size(20, 400)
        self.connect("delete-event", lambda w, e: w.hide() or True)

    def on_button_clicked(self, widget):
        print("Hello World")

    def on_tree_selection_changed(self, selection):
        hosts = []
        model, pathlist = selection.get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            hosts.append(model.get_value(tree_iter,0))
        self.main.Server.send(Packet.Packet(2, hosts))

    def on_switch_activated(self, switch, gparam):
        self.main.Server.send(Packet.Packet(3, switch.get_active()))

def show(win):
    win.show_all()