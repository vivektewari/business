
import logging
from datetime import datetime
Logger=logging
LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }
logging.basicConfig(filename='D:\\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business\logs\\businessLogging'+str((datetime.now()).strftime('%Y_%m_%d_%H_%M'))+'.log',level=LEVELS.get('critical', logging.NOTSET))

#Logger.disable(logging.INFO)
