from TinyCharm import time_util, file_utils
from TinyCharm.time_util import create_file_time_string
from TinyCharm.yaml_util import is_debug


class Logger:

    def __init__(self, TAG):
        self.TAG = TAG
        self.file_name = "log_" + create_file_time_string()

    @staticmethod
    def __red_text(text):
        return "\033[31m%s\033[0m" % text

    @staticmethod
    def __green_text(text):
        return "\033[32m%s\033[0m" % text

    @staticmethod
    def __yellow_text(text):
        return "\033[33m%s\033[0m" % text

    @staticmethod
    def __blue_text(text):
        return "\033[34m%s\033[0m" % text

    # 2022-01-24 16:50:11 | TAG
    def __process_data(self, message, level):
        text = time_util.get_time_string() + " | " + self.TAG + " | " + level + "  " + message
        if is_debug():
            file_utils.write_log(self.file_name, text + "\n")
        return text

    def error(self, message):
        print(self.__red_text(self.__process_data(message, "ERROR")))

    def error_(self, message, e: BaseException):
        print(self.__red_text(self.__process_data(message + "error message:" + e.args[0], "ERROR")))

    def warn(self, message):
        print(self.__yellow_text(self.__process_data(message, "WARN")))

    def success(self, message):
        print(self.__green_text(self.__process_data(message, "SUCCESS")))

    def info(self, message):
        print(self.__process_data(message, "INFO"))

# logger = Logger("ttt")
# logger.error("hello")
