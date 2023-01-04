import logging
import logging.handlers
import os


class customed_logger():
    def __init__(self,name,pathstring):
        logger=logging.getLogger(name)
        filename=f"log_{name}"
        logger.setLevel(logging.INFO)
        simple_formatter = logging.Formatter("[%(name)s] %(message)s")
        complex_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] - %(message)s"
        )
        
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(complex_formatter)
        console_handler.setLevel(logging.INFO)
        
        if os.path.isdir(pathstring):
            _path= os.path.join(pathstring,f'log_{name}.log')
        else:
            os.mkdir(pathstring) 
            _path  = os.path.join(pathstring,f'log_{name}.log')

        
        file_handler = logging.FileHandler(_path,mode="w")
        file_handler.setFormatter(complex_formatter)
        file_handler.setLevel(logging.DEBUG)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        self.logger=logger
        
    def logger_call(self):
        return self.logger
    
    



