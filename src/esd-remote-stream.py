#!/usr/bin/env python -i
from math import sin, cos, pi
import objc
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper
import time,os,subprocess

class EsdRemoteStream(NSObject):

    statusbar = None
    
    
    def applicationDidFinishLaunching_(self, notification):
        statusbar = NSStatusBar.systemStatusBar()
        # Create the statusbar item
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.statusitem.setHighlightMode_(1)
        self.statusitem.setToolTip_('EsdRemoteStream')
        self.statusitem.setTitle_('EsdRemoteStream')
        problems = []
        # do we have esd installed?
        if not  os.path.exists("/opt/local/bin/esd") :
            if not os.path.exists("/usr/local/bin/esd"):
                problems.append("esd")
        # do we have soundflower installed?
        if not  os.path.exists("/System/Library/Extensions/Soundflower.kext"):
            problems.append("soundflower")
        #problems.append("esd")
        #problems.append("soundflower")
        hide =  True if len(problems) >0 else False
        self.menu = NSMenu.alloc().init()
        #Quit Item
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menu.addItem_(menuitem)
        #Switch to Seperator
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Switch To:', '', '')
        menuitem.setHidden_(hide)
        self.menu.addItem_(menuitem)
        #Local item
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Local:', '', '')
        menuitem.setHidden_(hide)
        self.menu.addItem_(menuitem)
        #internal sound device
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('internal sound device', 'switchlocal:', '')
        menuitem.setHidden_(hide)
        self.menu.addItem_(menuitem)
        #Remote Seperator
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Remote:', '', '')
        menuitem.setHidden_(hide)
        self.menu.addItem_(menuitem)
        #Remote Items
        with open("hosts.conf") as hosts:
            for host in hosts.readlines():
                menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(host, 'switchremote:', '')
                menuitem.setHidden_(hide)
                self.menu.addItem_(menuitem)
                
        #Problems
        for problem in problems:
            menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Please install ' + problem + ' package', '', '')
            self.menu.addItem_(menuitem)
        
        
        # Bind it to the status item
        self.statusitem.setMenu_(self.menu)
    
    def kill(self):
        self.runshellscript("./killesd.sh")
    
    def switchlocal_(self,notused):
        self.kill()
        self.runshellscript("./audiodevice input 'internal'" )
        self.runshellscript("./audiodevice output 'internal'" )
    
    def switchremote_(self,item):
        self.kill()
        self.runshellscript("./audiodevice input 'Soundflower (2ch)'")
        self.runshellscript("./audiodevice output 'Soundflower (2ch)'")
        time.sleep(0.5)
        self.runshellscript(NSString.stringWithString_("./startesd.sh ") + item._.title)
    
    def runshellscript(self,script):
        print subprocess.call(script,shell=True)
    

if __name__ == "__main__":

    # set up system statusbar GUI
    app = NSApplication.sharedApplication()
    delegate = EsdRemoteStream.alloc().init()
    app.setDelegate_(delegate)

    AppHelper.runEventLoop()

