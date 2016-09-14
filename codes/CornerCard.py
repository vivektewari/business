from Card import Card
from interfaces_test import InterfaceError
from Logger import Logger
class CornerCard(Card):
    def __init__(self,amount,goToposition,*args):
        super(CornerCard,self).__init__(*args)
        self.amount=amount
        self.goToposition= goToposition
    def execute(self, player, dice=0):
        Logger.info("Player visited to "+str(self.name))
        if self.goToposition<>'False':
            Logger.info("player to go to position="+str(self.goToposition))
            position=int(self.goToposition)
            self.game.board[position].execute(player, dice)
        elif self.amount>0:
            player.obligation(self.game.banker,self.amount)
            Logger.info("player to pay="+str(self.amount))
            return True
        elif self.amount<0:
            Logger.info("player to receive=" + str(-self.amount))
            self.game.banker.transfer(player,-self.amount)

        else :
            InterfaceError("initializing a illegal Corner card")
            return False
        return True

