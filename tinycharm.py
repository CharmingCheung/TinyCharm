import os

import os.path
import traceback

import click
import tinify
from TinyCharm import csv_utils, file_utils, yaml_util
from TinyCharm.log_utils import Logger

version = "1.0.0"  # 版本

# 单个图片已经重试的次数
already_retry_count = 0

skip_size = yaml_util.skip_size()

# 是否遍历子目录
walk_sub_dir = yaml_util.walk_sub_dir()

logger = Logger("Main")


# 压缩的核心
def compress_core(input_file, output_file, img_width):
    if ".9.png" in input_file.lower():
        logger.warn("%s是点九图，跳过" % input_file)
        return
    input_file_size = file_utils.get_file_size(input_file)
    if input_file_size < skip_size:
        logger.warn("%s文件大小%s，不足%s，跳过" % (input_file, input_file_size, skip_size))
        return
    if not yaml_util.get_exclude_files(input_file):
        global already_retry_count
        set_key()
        inputMd5 = file_utils.get_file_md5(input_file)
        if not csv_utils.has_file(inputMd5):
            try:
                source = tinify.from_file(input_file)
            except tinify.errors.AccountError as e0:
                if e0.args[2] == 429:
                    logger.error('捕获到异常，API_KEY用完配额，尝试切换')
                    if yaml_util.next_key():  # 有其他key就切换重试
                        compress_core(input_file, output_file, img_width)
                    else:
                        raise Exception("API key全部都用完了，请重新配置后再使用")
            except Exception as e1:  # 其他错误，没办法避免，尝试
                if already_retry_count < yaml_util.get_retry_count():
                    already_retry_count = already_retry_count + 1
                    logger.error("执行第%s次重试" % already_retry_count)
                    compress_core(input_file, output_file, img_width)
                else:
                    raise e1
            else:
                already_retry_count = 0  # 重试数恢复为0
                if img_width != -1:
                    resized = source.resize(method="scale", width=img_width)
                    resized.to_file(output_file)
                else:
                    source.to_file(output_file)
                    file_md5 = file_utils.get_file_md5(output_file)
                    output_file_size = file_utils.get_file_size(output_file)
                    compress_ratio = file_utils.get_compression(input_file_size, output_file_size)
                    csv_utils.add_to_csv(file_md5, output_file, compress_ratio)
                    logger.success("完成：%s，原来MD5=%s，现在MD5=%s，压缩百分比=%s" % (
                        output_file, inputMd5, file_md5, compress_ratio))

        else:
            logger.warn("%s已存在，不进行压缩" % input_file)
    else:
        logger.warn("%s在例外列表里，不进行压缩" % input_file)


# 压缩一个文件夹下的图片
def compress_path(path, width):
    logger.info("compress_path-------------------------------------")
    if not os.path.isdir(path):
        logger.error("这不是一个文件夹，请输入文件夹的正确路径!")
        return
    else:
        fromFilePath = path  # 源路径
        toFilePath = path + "/" + yaml_util.get_output_file()  # 输出路径
        logger.info("fromFilePath=%s" % fromFilePath)
        logger.info("toFilePath=%s" % toFilePath)

        for root, dirs, files in os.walk(fromFilePath):
            logger.info("root = %s" % root)
            logger.info("dirs = %s" % dirs)
            logger.info("files= %s" % files)
            for name in files:
                fileName, fileSuffix = os.path.splitext(name)
                if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg' or fileSuffix == '.webp':
                    if not yaml_util.override_input_file():
                        toFullPath = toFilePath + root[len(fromFilePath):]
                        if os.path.isdir(toFullPath):
                            pass
                        else:
                            os.mkdir(toFullPath)

                    # 是否覆盖源文件
                    if yaml_util.override_input_file():
                        output_file = root + '/' + name
                    else:
                        output_file = root + "/" + yaml_util.get_output_file() + "/" + name
                    compress_core(root + '/' + name, output_file, width)
            for child in dirs:  # 遍历子目录
                if child != yaml_util.get_output_file() and walk_sub_dir and not yaml_util.get_exclude_dirs_name(
                        child):  # 要跳过输出目录
                    logger.info("正在遍历子目录：%s" % child)
                    compress_path(fromFilePath + "/" + child, width)
            break


# 仅压缩指定文件
def compress_file(input_file, width):
    logger.info("compress_file-------------------------------------")
    if not os.path.isfile(input_file):
        logger.error("这不是一个文件，请输入文件的正确路径!")
        return
    logger.info("file = %s" % input_file)
    dirname = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    fileName, fileSuffix = os.path.splitext(basename)

    # 是否覆盖源文件
    if yaml_util.override_input_file():
        output_file = input_file
    else:
        output_file = dirname + "/" + yaml_util.get_output_file() + "/" + basename

    if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg' or fileSuffix == '.webp':
        compress_core(input_file, output_file, width)
    else:
        logger.error("不支持该文件类型!")


@click.command()
@click.option('-f', "--file", type=str, default=None, help="单个文件压缩")
@click.option('-d', "--dir", type=str, default=None, help="被压缩的文件夹")
@click.option('-w', "--width", type=int, default=-1, help="图片宽度，默认不变")
def run(file, dir, width):
    logger.info("Charming's TinyPng V%s" % version)
    if file is not None:
        compress_file(file, width)  # 仅压缩一个文件
        pass
    elif dir is not None:
        compress_path(dir, width)  # 压缩指定目录下的文件
        pass
    else:
        for paths in yaml_util.read_input_dirs():
            compress_path(paths, width)
        # compress_path(os.getcwd(), width)  # 压缩当前目录下的文件
    logger.success("结束!")


# 设置tinypng key
def set_key():
    tinify.key = yaml_util.read_apikey()


if __name__ == "__main__":
    folder = os.path.exists(file_utils.get_cache_folder())  # 检查缓存路径
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(file_utils.get_cache_folder())

    try:
        run()
    except SystemExit:
        pass
    except BaseException as e:  # 包一层，用于输出日志
        logger.error("出错了~~" + traceback.format_exc())
        raise e
