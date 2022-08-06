import logging
import logging.handlers
import os


class customed_logger():
    def __init__(self,name,pathstring):
        logger=logging.getLogger(name)
        
        simple_formatter = logging.Formatter("[%(name)s] %(message)s")
        complex_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
        )
        
        
        console_handler = logging.StreamHandler(simple_formatter)
        console_handler.setFormatter(simple_formatter)
        console_handler.setLevel(logging.DEBUG)
        
        if os.path.isdir(pathstring):
            _path= os.path.join(pathstring,'log.log')
        else:
            _path  = pathstring
        
        file_handler = logging.FileHandler(_path)
        file_handler.setFormatter(complex_formatter)
        file_handler.setLevel(logging.ERROR)
        
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.setLevel(logging.WARNING)
        self.logger=logger
        
    def logger_call(self):
        return self.logger
    
    



