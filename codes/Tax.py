
from Card import Card
from Logger import Logger
class Tax(Card):
    def __init__(self,fixed,perSite,perHouse,perHotel,*args):
            self.fixed=fixed
            self.perSite=perSite
            self.perHouse=perHouse
            self.perHotel=perHotel
            super(Tax,self).__init__(*args)

    def execute(self, player, dice=0):
        Logger.info("Player visitet to Tax")
        amount=self.fixed+self.perSite*len(player.sites)+self.perHouse*player.purchase['house']+self.perHotel*player.purchase['hotel']
        Logger.info("player paid tax amounting to= "+str(amount))

        player.obligation(self.game.banker,amount)

