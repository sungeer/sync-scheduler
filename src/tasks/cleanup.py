from loguru import logger


# 定点任务 每天 02:00 跑一次
def daily_cleanup():
    logger.info('run daily_cleanup')
