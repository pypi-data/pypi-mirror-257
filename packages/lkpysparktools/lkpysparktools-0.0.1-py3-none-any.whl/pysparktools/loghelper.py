import logging

class LogHelper():
 
    _formatter = None
    _console_handler = None
    _logger = None
    
    @classmethod
    def create_formatter(cls):
        formatter = logging.Formatter(
            fmt = '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
            datefmt = '%Y-%m-%d %H:%M:%S'
        )
        
        return formatter
    
    @classmethod
    def formatter(cls):
        if(cls._formatter is None):
            cls._formatter = cls.create_formatter()

        return cls._formatter
    
    @classmethod
    def create_console_handler(cls):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(cls.formatter())
        
        return console_handler
    
    @classmethod
    def console_handler(cls):
        if(cls._console_handler is None):
            cls._console_handler = cls.create_console_handler()

        return cls._console_handler 
    
    @classmethod
    def get_logger_name(cls):
        return f'{cls.__name__}_{str(id(cls))}'
    
    @classmethod
    def create_logger(cls):
        logger = logging.getLogger(cls.get_logger_name())
        logger.setLevel(logging.DEBUG)
        logger.addHandler(cls.console_handler())
        return logger
    
    @classmethod
    def logger(cls):
        if(cls._logger is None):
            cls._logger = cls.create_logger()
        
        cls._logger.name = cls.get_logger_name()
        return cls._logger  
    
    