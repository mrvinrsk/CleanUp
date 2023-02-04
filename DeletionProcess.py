import os
import tempfile
from enum import Enum

from plyer import notification
import platform
from win10toast import ToastNotifier

import tkinter as tk
from Logger import CleanUpLogger
from Popup import show_text_popup
from util_functions import readable_bytes, delete_files

unix_home = os.path.expanduser("~")
windows_home = os.environ['USERPROFILE']
localappdata = os.environ['LOCALAPPDATA']


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
        os.path.join(unix_home, 'Library/Caches/Google/Chrome/Default/Cache'),  # MacOS
        os.path.join(unix_home, '.cache/google-chrome'),  # Linux
        os.path.join(localappdata, r'Google\Chrome\User Data\Default\Cache'),  # Windows

        # Firefox
        os.path.join(unix_home, 'Library/Caches/Firefox'),  # MacOS
        os.path.join(unix_home, '.mozilla/firefox'),  # Linux
        os.path.join(localappdata, r'mozilla-temp-files'),  # Windows

        # Edge
        os.path.join(unix_home, 'Library/Caches/Microsoft Edge Dev/Default/Cache'),  # MacOS
        os.path.join(unix_home, '.config/Microsoft Edge Dev/Default/Cache'),  # Linux
        os.path.join(localappdata, r'Microsoft\Edge\User Data\Default\Cache'),  # Windows

        # Safari
        os.path.join(unix_home, 'Library/Caches/com.apple.Safari/'),  # MacOS

        # Opera
        os.path.join(unix_home, 'Library/Caches/com.operasoftware.Opera'),  # MacOS
        os.path.join(unix_home, '.config/opera'),  # Linux
        os.path.join(localappdata, r'Opera Software\Opera Stable\Cache'),  # Windows
    ]


class DeletionProcess:
    id_counter = 0

    def __init__(self, types, show_details_after=False):
        DeletionProcess.id_counter += 1

        self.id = DeletionProcess.id_counter
        self.logger = CleanUpLogger()
        self.types = types
        self.show_details_after = show_details_after

        self.was_executed = False
        self.deleted_bytes = None
        self.checked_paths = None


    def get_deleted_bytes(self):
        if self.was_executed:
            return self.deleted_bytes
        return -1

    def get_deleted_files(self):
        if self.was_executed:
            return self.deleted_files
        return -1

    def get_checked_paths(self):
        if self.was_executed:
            return self.checked_paths
        return []

    def show_details(self):
        self.logger.info("Opening detail window")

        details = tk.Tk()
        details.title("CleanUp Information for id " + str(self.id))

        screen_width = details.winfo_screenwidth()
        screen_height = details.winfo_screenheight()

        width = 750
        height = 300

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        details.geometry("%dx%d+%d+%d" % (width, height, x, y))

        tk.Frame(details, padx=10, pady=10).pack()

        tk.Label(details, text="Deleted bytes: " + readable_bytes(self.get_deleted_bytes())).pack()
        tk.Label(details, text="Checked paths: " + ", ".join(self.get_checked_paths())).pack()

        details.mainloop()

    def delete(self):
        if len(self.types) == 0:
            show_text_popup("CleanUp", "Please select at least one option.")
            self.logger.info("Tried to start a deletion process without specifying a type.")
            return

        self.was_executed = True
        self.logger.info("Starting deletion process with id " + str(self.id))
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

        self.deleted_bytes = total_deleted_bytes
        self.checked_paths = search_paths

        if total_deleted_bytes > 0:
            if self.show_details_after:
                self.show_details()
            else:
                notification.notify(
                    title="Freed up",
                    message="We've freed up " + str(readable_bytes(total_deleted_bytes)) + " of space.",
                    app_name="CleanUp",
                    timeout=5,
                    callback=self.show_details
                )

        else:
            notification.notify(
                title="Nothing to delete",
                message="There was nothing else to delete left.",
                app_name="CleanUp",
                timeout=5
            )
