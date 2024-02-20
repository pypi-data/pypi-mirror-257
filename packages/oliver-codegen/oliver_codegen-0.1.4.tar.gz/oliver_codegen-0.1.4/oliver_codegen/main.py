from oliver_codegen.service.argsparse import ArgumentParser, HandleArgs


def start():
    """
    项目开始入口
    :return: None
    """
    # 获取命令行参数
    args_parser = ArgumentParser()
    args = args_parser.parse()
    # 处理命令行参数
    handle_args = HandleArgs(args=args)
    handle_args.handle()
