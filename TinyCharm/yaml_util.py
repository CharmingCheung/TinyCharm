import yaml

from TinyCharm import file_utils


def _get_yaml_entity():
    with open(file_utils.get_root_path() + "/config/config.yaml", "r", encoding="UTF-8") as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


api_key_position = 0


# 读取配置的api_key
def read_apikey():
    return _get_yaml_entity()['api_keys'][api_key_position]


def next_key():
    global api_key_position
    if len(_get_yaml_entity()['api_keys']) > api_key_position + 1:
        api_key_position = api_key_position + 1
        print("key切换为:%s" % read_apikey())
        return True
    else:
        return False


# 读取配置的需压缩文件夹列表
def read_input_dirs():
    return _get_yaml_entity()['file_dirs']


# 获取重试次数
def get_retry_count():
    return


# 读取例外列表
def get_exclude_files(file_path):
    return file_path in _get_yaml_entity()['exclude_files']


# 读取例外文件夹名
def get_exclude_dirs_name(file_path):
    return file_path in _get_yaml_entity()['exclude_dirs_name']


# 是否覆盖源文件
def override_input_file():
    return _get_yaml_entity()['override_input_file']


# 输出文件夹名 注意不是路径，是在与源文件同级的文件夹名
def get_output_file():
    return _get_yaml_entity()['output_folder_name']


# 源文件大小少于此数值自动跳过，单位byte
def skip_size():
    return _get_yaml_entity()['skip_size']


# 是否遍历子目录
def walk_sub_dir():
    return _get_yaml_entity()['walk_sub_dir']


# 是否debug模式，开启即输出日志到本地
def is_debug():
    return _get_yaml_entity()['debug']
