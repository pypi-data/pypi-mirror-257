import logging
from oliver_codegen.core.params import pyproject_toml_params

"""
Python logging 模块, 主要包括四个组件:

Loggers:记录器,提供应用程序代码能直接使用的接口;
Handlers:处理器,将记录器产生的日志发送至目的地;
Filters (可选):过滤器,提供更好的粒度控制,决定哪些日志会被输出;
Formatters:格式化器，设置日志内容的组成结构和消息字段

创建Logger --> 创建StreamHandler(屏幕) 或者 创建FileHandler(文件) --> 设置日志等级 --> 创建Formatter -->

用formatter渲染所有的Handler --> 将所有的Handler加入logger内 --> 程序调用logger
"""

# -----------------------------------------------------------------------------------------

"""
logger 记录器

1.提供应用程序调用的logger接口 (logger 是单例)
logger = logging.getLogger(__name__)

2.决定日志记录的级别
logger.setLevel()

3.将日志内容传递到相关联的handlers中
logger.addHandler()
或者删除:
logger.removeHandler()

"""

# -----------------------------------------------------------------------------------------

"""
Handlers 处理器
将日志分发到不同的目的地, 比如标准输出, 文件, 邮件或者通过socket, http等协议发送到任意地方.
主要包括: StreamHandler, FileHandler, BaseRotatingHandler, RotatingFileHandler, TimedRotatingFileHandler,
SocketHandler, SMTPHandler, HTTPHandler, QueueHandler等

StramHandler
标准输出 stdout (比如屏幕) 分发器.
sh = logging.StreamHandler(Stream=None)

FileHandler
将日志保存到磁盘的处理器.
fh = logging.FileHandler(filename, mode='a', encoding='utf-8', delay=False)

通过 setFormatter() 设置当前handler对象使用的消息输出格式
"""

# -----------------------------------------------------------------------------------------

"""
Formatters 格式化日志消息
Formatter 对象用来最终设置日志信息的输出顺序, 结构和内容

初始化:
ft = logging.Formatter(fmt=None, datefmt=None, style= ' %')

datefmt默认输出格式: %Y-%m-%d %H:%M:%S" -> "年-月-日 小时-分钟-秒
style参数默认为 % 百分号, 这表示 %()s格式方式. 例如 %(levelname)s

levelname: 日志级别名称(Debug, Info, Warning, Error, Critical)
levelno: 日志对应的数值
name: 日志调用者
pathname: 生成日志的文件的完整路劲
message: 打印信息
asctime: 日志打印时间
msecs: 日志生成时间部位的毫秒部分
module: 生成日志的模块名称
filename: 打印日志的所在文件夹
lineno: 该日志的所在行号
funcName: 调用日志的函数名称
process: 生成日志的进程ID
processName: 进程名
thread: 生成日志的线程ID
threadName: 生成日志的线程名
"""

# -----------------------------------------------------------------------------------------

"""
简单的使用
logging.basicConfig(format='%(levelname)s%(message)s', level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
logging.info("我只一条info日志")
"""

"""
日志级别数值:
logging.DEBUG = 10, 
logging.INFO = 20, 
logging.WARNING = 30, 
logging.ERROR = 40, 
logging.CRITICAL = 50
"""

# logger 记录器
# 如果 logging.getLogger() 中的参数不填, 默认为root, 日志打印级别为 warning
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# handler 处理器
# 控制台处理器
consoleHandler = logging.StreamHandler()
# 如果 handler 没有设置输出级别, 默认使用 logger的级别
# 如果 handler 想设置级别生效, logger的级别数值必须小于 handler 的.
# 比如 handler 设置的 Debug 级别, 如果 logger 是默认warning级别, 那么最终会选择 logger
# 因为logging的 warning 数值为 30, 而handler的debug数值为10, 30 > 10, 最终选择的logging的.
# 所以 logger 和 handler 级别相比, 哪个大就选择那个.
consoleHandler.setLevel(level=logging.DEBUG if pyproject_toml_params.debug else logging.INFO)

# 文件处理器, 如果没有设置.setLevel级别, 默认使用logger的级别.
# fileHandler = logging.FileHandler(filename='task-handle.log', mode='a', encoding='utf-8')
# fileHandler.setLevel(logging.INFO)

# formatter 格式
# %(levelname)-8s 中的 -8 表示, 左对齐, 占8位字符
formatter = logging.Formatter('%(levelname)s::%(message)s')

# 过滤器
# flt = logging.Filter(__name__)

# 给handler处理器设置输出格式
consoleHandler.setFormatter(formatter)
# fileHandler.setFormatter(formatter)

# 给logger添加处理器
# logger 可以添加多个处理器, 如果添加多个则会同时想两个handler处理器添加日志
# 比如 logger.addHandler(fileHandler) 和 logger.addHandler(consoleHandler) 同时添加
# 则最后日志会同时写入控制台 和 文件里面.
logger.addHandler(consoleHandler)



