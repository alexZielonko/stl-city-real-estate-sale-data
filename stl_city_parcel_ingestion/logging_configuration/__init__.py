import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'runtime_info.log',
        },
        'migration': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'migration_info.log',
        }
    },
    'loggers': {
        '': {
            'handlers': ['debug', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'migration': {
            'handlers': ['debug', 'migration'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}


def initialize_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger()
    log.debug("Logging is configured.")
