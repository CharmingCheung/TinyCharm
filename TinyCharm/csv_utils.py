import pandas as pd

from TinyCharm import file_utils
from TinyCharm import time_util


# csv路径
def get_csv_location():
    return file_utils.get_root_path() + "/cache/md5.csv"


# 插入到csv中
def add_to_csv(md5str, file_path, compress_ratio):
    needHeader = False
    try:  # 先读表 如果不正常 那需要添加表头
        pd.read_csv(get_csv_location())
    except BaseException:
        needHeader = True
    finally:
        time_string = time_util.get_time_string()
        columns_config = ['md5', 'file_path', 'compress_ratio', 'date_time']
        df_temp = pd.DataFrame([[md5str, file_path, compress_ratio, time_string]],
                               columns=columns_config)
        df = pd.DataFrame(columns=columns_config)
        df = pd.concat([df, df_temp], ignore_index=True)
        df.to_csv(get_csv_location(), mode='a', header=needHeader, index=False)


# 查询csv 是否已经压缩过此文件
def has_file(md5str):
    try:
        df = pd.read_csv(get_csv_location())
    except BaseException:  # 有可能文件都没有，直接跳过
        return False
    return len(df[df['md5'] == md5str].index.tolist()) > 0
    # df = pd.read_csv(get_csv_location())
    # print(len(df[df['md5'] == md5str].index.tolist()) > 0)

# has_file('')
