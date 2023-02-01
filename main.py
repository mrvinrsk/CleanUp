import os
import tempfile
from util_functions import *
from plyer import notification

home = os.path.expanduser("~")
directories = [
    # linux
    '/tmp',
    '/var/tmp',
    # windows
    tempfile.gettempdir()
]

deletedBytes = 0
for directory in directories:
    deletedBytes += int(delete_files(directory))

notification.notify(
    title="Freed up",
    message="We've freed up " + str(readable_bytes(deletedBytes)) + " of space.",
    app_name="CleanUp",
    timeout=5
)
