
import logging
from datetime import datetime
Logger=logging
LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }
logging.basicConfig(filename='D:\\vivek\\Business\\monopolyfiles\\logs\\businessLogging'+str((datetime.now()).strftime('%Y_%m_%d_%H_%M'))+'.log',level=LEVELS.get('critical', logging.NOTSET))

#Logger.disable(logging.INFO)
