import os
import tempfile
from enum import Enum

from Logger import CleanUpLogger

unix_home = os.path.expanduser("~")
windows_home = os.environ['USERPROFILE']


class Type(Enum):
    TEMP = [
        '/tmp',
        '/var/tmp',
        tempfile.gettempdir()
    ]
    DOWNLOAD = [
        os.path.join(windows_home, 'Downloads'), os.path.join(unix_home, 'Downloads')
    ]
    BROWSER_DATA = [
        # Chrome
        os.path.join(windows_home, r'AppData\Local\Google\Chrome\User Data\Default'),
        os.path.join(unix_home, '.config/google-chrome/Default'),

        # Firefox
        os.path.join(windows_home, r'AppData\Roaming\Mozilla\Firefox\Profiles'),
        os.path.join(unix_home, '.mozilla/firefox'),

        # Edge
        os.path.join(windows_home, r'AppData\Local\Microsoft\Edge\User Data\Default'),
        os.path.join(unix_home, 'Library/Application Support/Microsoft Edge/Default'),

        # Safari
        os.path.join(windows_home, r'AppData\Roaming\Apple Computer\Safari'),
        os.path.join(unix_home, 'Library/Safari'),

        # Opera
        os.path.join(windows_home, r'AppData\Roaming\Opera Software\Opera Stable'),
        os.path.join(unix_home, '.config/opera')
    ]


class DeletionProcess:
    def __init__(self, types):
        self.logger = CleanUpLogger()
        self.types = types

    def delete(self):
        self.logger.warning('Removing files of the following types: ' + ", ".join(map(lambda _type: _type.name, self.types)))
        pass
