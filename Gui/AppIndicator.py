import AttackWindow
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
import os
import threading
import notify2
from threading import Thread

class AppIndicator(Thread):

    def __init__(self, main):
        Thread.__init__(self)
        self.main = main
        self.APPINDICATOR_ID = 'NetworkLiberatorV2'
        notify2.init(self.APPINDICATOR_ID)

    def run(self):
        self.indicator = appindicator.Indicator.new(self.APPINDICATOR_ID, os.path.abspath('./Gui/Assets/NetworkLiberator.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()
        self.item_quit = Gtk.MenuItem('Close')
        self.item_quit.connect('activate', quit)

        self.item_attack_window = Gtk.MenuItem('Attack...')
        self.item_attack_window.connect('activate', self.open_attack_window)

        self.menu.append(self.item_attack_window)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(self.item_quit)
        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        print("Run Indicator")
        Gtk.main()

    def notify_attack_incoming(self, param):
        n = notify2.Notification(param['title'], param['content'], os.path.abspath('./Gui/Assets/error-flat.png'))
        n.set_category("network.error")
        n.show()
    
    def stop(self):
        Gtk.main_quit()

    def open_attack_window(self,source):
        AttackWindow.show(self.main.AttackWindow)

def quit(source):
    Gtk.main_quit()