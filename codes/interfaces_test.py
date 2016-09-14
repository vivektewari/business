










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






from Site import Site
from CitiSite import CitiSite
from Player import Player
from Banker import Banker
from Game import  Game
import Brain
class InterfaceError(Exception):
    def __init__(self,value):self.value=value


game=Game()
player1= Player(brain=(Brain.pureRandom,[game]),name='vivek', cash=100, game=False)
player2= Player(brain=(Brain.pureRandom,[game]),name='abhishek', cash=200, game=False)
game.banker= Banker(name='banker', cash=100, game=False)
site1= CitiSite(50,50,20,30,40,50,60,13, 2, 20, 100, 10, 30, 'mumbai', 24,game)  #__init__(self,group,groupCount,groupRent,cost,baseRent,mortgage,*args)
site2= Site(13, 2, 30, 100, 10, 30, 'kolkata', 25,game)  #__init__(self,group,groupCount,groupRent,cost,baseRent,mortgage,*args):
#game.makeBoard('D:\Users\\703145584\\Documents\\Genpact_Internal\\adhoc\\business')



instanceSet=[player1,site1]
def checkInterface(cls,variable,value):

    for element in instanceSet:
        if str(element.__class__.__name__)==cls:
            if variable in element.__dict__.keys():
                if type(value)==type(element.__dict__[variable]):return True
                else:raise InterfaceError('variable type not matching')
            else: raise InterfaceError('undefined variable')
    return InterfaceError("undefined class")







#checkInterface(Site,"group")
# class w(object):
#     def __init__(self,a):self.a=a
#     print "thatsit"
#     def func(a,b):return a-b
#     def fre(self):"me here"
#
#
#
# for key,value in w.__dict__.items():
#     print "\n key="+key +"\n"
#     print value
#     print type(value)
#     if key=='__weakref__':
#         if isinstance(value,dict):
#             for key,value in value.items():
#                 print key
#                 print value
#                 print "\n"
#