from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading

###
# This class allows to restore the application window after closing it by putting it in the windows tray.
###
class TrayIconHandler:
    def __init__(self, app_name, icon_path, on_restore, on_exit):
        self.app_name = app_name
        self.icon_path = icon_path
        self.on_restore = on_restore
        self.on_exit = on_exit
        self.icon = None
        
    def create_icon(self):
        icon_image = Image.open(self.icon_path)
        
        menu = Menu(
            MenuItem("Restore", self.on_restore),
            MenuItem("Exit", self.on_exit)
        )
        
        self.icon = Icon(self.app_name, icon_image, self.app_name, menu)
        
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def stop(self):
        if self.icon:
            self.icon.stop()
            self.icon = None