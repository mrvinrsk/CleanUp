import logging
import os
import time
import locale

date_formats = {
    'default': '%m/%d/%Y | %I:%M:%S %p',
    'de_DE': '%d.%m.%Y | %H:%M:%S',
    'en_US': '%m/%d/%Y | %I:%M:%S %p',

    # add more language codes as needed
}


# TODO: Fix Singleton
class CleanUpLogger:
    def __init__(self, level=logging.INFO, file_name='latest.log'):

        language = locale.getlocale()[0]
        date_format = date_formats.get(language, date_formats['default'])

        self.logger = logging.getLogger('CleanUp')
        self.logger.setLevel(level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=date_format)
        console_handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(console_handler)

            self.file_name = file_name
            self.check_and_rename_file()

            file_handler = logging.FileHandler(self.file_name)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        else:
            del self

    def check_and_rename_file(self):
        if os.path.exists(self.file_name):
            stat = os.stat(self.file_name)
            mod_time = stat.st_mtime
            current_time = time.time()

            if current_time - mod_time >= 2 * 60 * 60:  # 2 hours
                rename_to = "log-{}.log".format(time.strftime("%Y-%m-%d-%H-%M", time.gmtime(mod_time)))
                os.rename(self.file_name, rename_to)
                self.file_name = 'latest.log'

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)
