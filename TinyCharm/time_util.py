import time


def get_time_string():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def create_file_time_string():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())
