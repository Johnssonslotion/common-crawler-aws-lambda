import cbase
import logging
from logging.handlers import TimedRotatingFileHandler
import os






if __name__ == "__main__":
    '''
    실질 task flow는 이쪽에서 작성예정
    
    
    '''
    logger = logging.getLogger(__name__)
    FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format=FORMAT)
    logging.info('START Crawling')
    
    
    log_dir = './logs'

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)


    