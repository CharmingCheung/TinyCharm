# TinyCharm

在 [GcsSloop/TinyPng](https://github.com/GcsSloop/TinyPng) 的基础上二次开发，调用TinyPng
API，实现自动化压缩图片脚本。支持配置多个常用目录，自动跳过已压缩过的图片，支持配置多ApiKey自动切换

平时主要都是写Java和Kotlin，在做这个之前完全没学过Python，好多逻辑可能会用了一些取巧的方法。如果有习惯或者语法或者重大的常识问题问题，望见谅！

## Feature

- 使用 csv 记录已经压缩过的图片信息，包括路径、MD5、压缩率、日期。后续遇到相同MD5的图片会自动绕过，减少重复压缩
- 压缩错误重试，可配置单个图片重试数量，达到最大重试数即抛出异常
- ApiKey配额满自动切换ApiKey
- 支持配置是否覆盖源文件，或者在源文件目录下创建一个压缩目录
- 不压缩点九图
- 支持配置是否遍历子目录
- 支持配置调用压缩的源文件大小阈值，少于此大小的文件跳过压缩
- 支持输出日志到本地，便于排查问题

## TODO

- 配置上次压缩率未够低的情况下是否继续压缩

## Usage

### 开发环境

Python 3.9

### 安装依赖

```shell
  pip3 install --upgrade tinify pandas pyyaml click
```

### 配置config/config.yaml

```yaml
# 配置多api_keys
api_keys:
  - 'xxxxxxxxxxxx'
  - 'xxxxxxxxxxxx'

#调试模式，开启将会记录日志到本地
debug: true

#重试次数
retry_count: 3

#是否覆盖源文件
override_input_file: false

#源文件大小少于此数值自动跳过，单位byte
skip_size: 0

#是否遍历子目录，会自动跳过[output_folder_name]下的文件
walk_sub_dir: true

#输出文件夹名
#当override_input_file为False时才生效。会在源文件目录创建[output_folder_name]文件夹
output_folder_name: "output"

# 配置多路径
# 如在Windows环境下使用，记得把路径的"\"改为"/"或者"\\"
# 支持相对路径和绝对路径
file_dirs:
  - "/Users/charming/Desktop/图片压缩测试/1"
  - "/Users/charming/Desktop/图片压缩测试/2"

# 配置例外文件名，不对此列表的图片压缩
# 如在Windows环境下使用，记得把路径的"\"改为"/"或者"\\"
exclude_files:
  - "/Users/charming/Desktop/图片压缩测试/2/av_bg_untion_rank_success_promote.png"

#配置例外的目录名，不对此文件夹和它的子目录进行压缩
#注意是文件夹名，不是路径
exclude_dirs_name:
  - ".git"
  - "build"
  - ".gradle"
  - ".idea"

```

### 支持参数


|  参数  | 参数类型 | 摘要                          | 示例                                                                                       |
|:----:|------|-----------------------------|------------------------------------------------------------------------------------------|
|  无参  |      | 压缩`config/config.yaml`配置的路径 | `tinycharm.py`                                                                           |
| `－f` | 图像文件 | 压缩指定的单个文件                   | `tinycharm.py -f /Users/charming/Desktop/图片压缩测试/2/av_bg_untion_rank_success_promote.png` |
| `－d` | 文件夹  | 压缩指定文件夹下所有图片文件              | `tinycharm.py -d /Users/charming/Desktop/图片压缩测试/1`                                       |
| `-w` | 整型数字 | 压缩后图片的宽度，不指定则宽度不变           | `tinycharm.py -w 300`                                                                    |


