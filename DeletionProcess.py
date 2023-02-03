import os
import tempfile
from enum import Enum

from plyer import notification

from Logger import CleanUpLogger
from util_functions import readable_bytes, delete_files

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
        if len(self.types) == 0:
            self.logger.info("No deletion types selected.")
            return

        self.logger.warning('Removing files of the following types: ' + ", ".join(map(lambda _type: _type.name, self.types)))

        total_deleted_bytes = 0
        for _type in self.types:
            search_paths = []

            for path in _type.value:
                if path not in search_paths:
                    if os.path.exists(path):
                        search_paths.append(path)

            self.logger.warning('Start removing files of type ' + _type.name + ' in paths: ' + ", ".join(search_paths))

            for path in search_paths:
                result = delete_files(path)
                deleted_bytes = result[0]
                deleted_files = result[1]
                total_deleted_bytes += deleted_bytes
                self.logger.info('Removed ' + readable_bytes(deleted_bytes) + ' in ' + path + ' by removing ' + str(deleted_files) + ' file' + ('s' if deleted_files != 1 else '') + '.')

        notification.notify(
            title="Freed up",
            message="We've freed up " + str(readable_bytes(total_deleted_bytes)) + " of space.",
            app_name="CleanUp",
            timeout=5
        )
