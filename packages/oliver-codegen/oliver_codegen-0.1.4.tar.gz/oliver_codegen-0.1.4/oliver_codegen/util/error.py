from oliver_codegen.core.log import logger


def error_exit(msg: str, excp=None):
    if excp is not None:
        logger.error(msg, excp)
        exit(-1)
    logger.error(msg)
    exit(-1)
