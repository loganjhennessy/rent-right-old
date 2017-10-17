import logging

logfile = '/home/lhennessy/rent-scraper/rentscraper/scraper.log'

def get_configured_logger(level, name):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging,level))

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

    return logger
