
from Card import Card
import logging
from Logger import Logger
class Jail(Card):
    def __init__(self, amount, *args):
        super(Jail,self).__init__(*args)
        self.amount=amount
    def execute(self, player, dice=0):
        Logger.info("Player visited to jail")
        if player.jailPass>0:
            player.jailPass-=1
            Logger.info('player has the jail pass ')
            return True
        else:
            if player.jailChoice(self.amount):
                Logger.info("player paid the jail fees so didnt go to jail=" + str(self.amount))
                return True
        logging.info(str(player.name)+" went  to jail")
        self.game.jail[player]=0
        return True




