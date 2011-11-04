'''
Minimal setup.py example, run with:
% python setup.py py2app
'''

from distutils.core import setup
import py2app

NAME = 'EsdRemoteStream'
SCRIPT = 'esd-remote-stream.py'
VERSION = '0.1'
ID = 'esd-remote-stream'
DATA_FILES = ['killesd.sh','startesd.sh','hosts.conf','audiodevice']
plist = dict(
     CFBundleName                = NAME,
     CFBundleShortVersionString  = ' '.join([NAME, VERSION]),
     CFBundleGetInfoString       = NAME,
     CFBundleExecutable          = NAME,
     CFBundleIdentifier          = '%s' % ID,
     LSUIElement                 = '1'
)

app_data = dict(script=SCRIPT, plist=plist)

setup(
   app = [app_data],
   data_files =DATA_FILES
)

