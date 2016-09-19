#not in use
import logging
from datetime import datetime
gameLogger = logging.getLogger('simple_logger')
hdlr_1 = logging.FileHandler('D:\\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business\logs\\gameLogger'+str((datetime.now()).strftime('%Y_%m_%d_%H_%M'))+'.log',mode='w')
# hdlr_1.setFormatter('%(asctime)s : %(message)s')
# streamHandler = logging.StreamHandler()
# streamHandler.setFormatter('%(asctime)s : %(message)s')
gameLogger.addHandler(hdlr_1)
# gameLogger.addHandler(streamHandler)
gameLogger.setLevel(logging.DEBUG)
