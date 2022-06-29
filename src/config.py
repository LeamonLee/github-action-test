from pymongo import MongoClient
import os, datetime, logging
TW_TZ = datetime.timezone(datetime.timedelta(hours=+8))     # 設定為 +8 時區


FORMAT = '%(asctime)s - [%(module)s] - %(levelname)s - [%(lineno)d] - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'normal': {  # the name of formatter
            # 'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            # 'datefmt': '%Y-%m-%d %H:%M:%S'
            'format': logging.Formatter(FORMAT, DATE_FORMAT)
        }
    },
    'handlers': {
        'file': {  # the name of handler
            'class': 'FileHandler',  # the log rotation by time interval
            'filename': 'f3.log',  # the path of the log file
            'when': 'midnight',  # time interval
            'formatter': 'normal',  # use the above "normal" formatter
        },
        'console':{

        }
    },
    'loggers': {
        'logger2': {  # the name of logger
            'handlers': ['time-rotating-file2'],  # use the above "time-rotating-file2" handler
            'level': 'DEBUG',  # logging level
            'propagate': True
        }
    },
}