#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#https://stackoverflow.com/questions/6389580/quick-and-easy-trayicon-with-python/33069455#33069455
import wx
import Twitchcheck
import webbrowser
import os
from thread import start_new_thread

print "mem"
TRAY_TOOLTIP = 'PyChecker'
TRAY_ICON = os.path.join(os.path.dirname(__file__), 'quader.png')

def create_menu_item(menu, label, func, *args):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, lambda evt, temp=args: func(args[0]), id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        print TRAY_ICON
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        for channel in Twitchcheck.dictionary.values():
            create_menu_item(menu,' {0:<20}     {1:<7}    {2}'.format(channel['name'],channel["viewers"],channel['game']),self.openinbrowser,channel['urlname'])
        create_menu_item(menu, 'Exit', self.on_exit,0)

        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print "Tray icon was left-clicked."
        Twitchcheck.showList()

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def openinbrowser(self,name):
        webbrowser.open_new_tab("https://www.twitch.tv/{}".format(name))

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    print "MEEEM"
    app = App(False)
    start_new_thread(Twitchcheck.startMainLoop,())
    app.MainLoop()

print "meem"
if __name__ == '__main__':
    main()
