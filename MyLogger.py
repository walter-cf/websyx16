import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # relationship mapping

    def __init__(self, filename, level='info', when='D', backCount=15,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # Setting the log format
        self.logger.setLevel(self.level_relations.get(level))  # Setting the log level
        console_handler = logging.StreamHandler()  # on-screen output
        console_handler .setFormatter(format_str)  # Setting the format
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,encoding='utf-8')  # automatically generates the file at specified intervals
        th.setFormatter(format_str)  # Setting the format
        self.logger.addHandler(console_handler)  # Add the object to the logger
        self.logger.addHandler(th)

    def loggingError(self, *args):
        self.logger.error(args)
        
    def loggingWarn(self, *args):
        self.logger.warning(args)
        
    def loggingInfo(self, *args):
        self.logger.info(args)
        
    def loggingDebug(self, *args):
        self.logger.debug(args)
        
    def loggingCrit(self, *args):
        self.logger.critical(args)
        
    def loggingTrace(self, *args):
        self.logger.debug(args)
