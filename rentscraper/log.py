import logging
import os

loggers = {}

def get_configured_logger(level, name):

    dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))
    logfile = dir_path + '/logs/' + name + '.log'

    if loggers.get(name):
        return loggers.get(name)

    else:
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging,level))
        
        if not logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(getattr(logging,level))

            fh = logging.FileHandler(logfile)
            fh.setLevel(getattr(logging,level))

            format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(format_string)

            ch.setFormatter(formatter)
            fh.setFormatter(formatter)

            logger.addHandler(ch)
            logger.addHandler(fh)

        loggers.update(dict(name=logger))

        return logger
