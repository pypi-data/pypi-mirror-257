import os
import sys

from loguru import logger


def setup_logger(log_file, project_name):
    """
    设置日志记录器
    :param log_file: 日志文件路径
    :param project_name: 项目名称
    """
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    logger.remove()
    logger.add(
        log_file,
        rotation="10 MB",
        compression="zip",
        # serialize=True,
        format="{time:YYYY-MM-DD HH:mm:ss}-{level}-{message}",
    )
    logger.add(sys.stdout, level="INFO")
    logger.bind(project=project_name)


def log_info(message):
    """
    记录信息级别的日志
    """
    logger.info(message)


def log_warning(message):
    """
    记录警告级别的日志
    """
    logger.warning(message)


def log_error(message):
    """
    记录错误级别的日志
    """
    logger.error(message)
