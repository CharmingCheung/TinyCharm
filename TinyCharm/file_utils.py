import hashlib
import os


def get_root_path():
    return os.path.abspath(os.path.dirname(__file__)) + "/.."


def get_cache_folder():
    return get_root_path() + "/cache/"


def get_file_md5(file):
    with open(file, 'rb') as fp:
        data = fp.read()
        return hashlib.md5(data).hexdigest()


def get_file_size(file):
    return os.stat(file).st_size


# 计算压缩率
def get_compression(input_size, output_size):
    return "%.2f%%" % ((input_size - output_size) / input_size * 100)


# 写入文本到文件里
def write_log(fileName, text):
    if not os.path.exists(get_root_path() + "/logs/"):
        os.mkdir(get_root_path() + "/logs/")
    append_to_file(get_root_path() + "/logs/" + fileName, text)


# 写入文本到文件里
def append_to_file(fileName, text):
    with open(fileName, "a") as file_object:
        # Append 'hello' at the end of file
        file_object.write(text)
