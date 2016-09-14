
from abc import ABCMeta
from Logger import Logger

from Card import Card


class Site(Card):
    def __init__(self,group,groupCount,groupRent,cost,baseRent,mortgage,*args):
        """
        :param group: (groupIndex:integer,groupRent,minGroupCards:integer)
        :param cost: integer
        :param baseRent: integer
        :param mortgage: set(Site)
        :param args:see Card
        :return:Site
        """
        self.group=(group,groupCount,groupRent)
        self.cost=cost
        self.baseRent=baseRent
        self.rent=baseRent
        self.mortgage=mortgage
        self.sellingCost=cost
        super(Site,self).__init__(*args)


    def execute(self, player, dice=0):
        Logger.info(str(self.name) + " visited " )
        if self.owner==player:
            Logger.info("visited in own site so no transaction happens")
            return False
        elif self.owner==self.game.banker:
                if player.buySite(self):
                    Logger.info("player bought the site by paying amount as cost="+str(self.sellingCost))
                    return True
        player.obligation(self.owner,self.rent)
        Logger.info("player paid the rent=" + str(self.rent))
        if self.owner<>self.game.banker:
            paymentToBank=0
            if self  in self.owner.mortgage.keys():
                paymentToBank+=0.5*self.rent
                Logger.info("owner to transfer 50% of the rent as the site was in mortgage")
            if self.owner in self.game.jail.keys():
                paymentToBank+=0.1*min(paymentToBank,self.rent)
                Logger.info("owner to transfer 10 % of its income as owner in jail")
            self.owner.obligation(self.game.banker,int(paymentToBank))
            if paymentToBank<>0:Logger.info("owner transfering jail/mortgage charges to bank on rent earning ="+str(int(paymentToBank)))
        return True



    def updateRent(self):
        oldRent=self.rent
        if str(self.owner.__class__.__name__)<>'Banker':
            if self in self.owner.completeSites:
                self.rent=self.group[2]
        if oldRent<>self.rent:Logger.info(str(self.name)+"rent updated to ="+str(self.rent))
        return oldRent<>self.rent

    def changeOwner(self,owner):
        if self.owner<>owner:
            if str(self.owner.__class__.__name__) == 'Player' :
                if self in self.owner.mortgage.keys(): del self.owner.mortgage[self]
                if self in self.owner.completeSites:self.owner.completeSites.remove(self)

            self.owner.sites.remove(self)
            self.owner=owner
            self.owner.sites.append(self)
            Logger.info(str(self.name)+" owner changed to="+str(owner.name))

if __name__ == '__main__':
    import unittest
    from interfaces_test import checkInterface

    class TestSite(unittest.TestCase):
        from interfaces_test import player1,player2,game,banker
        site= Site(13, 2, 20, 0, 0, 100, 'mumbai', player1, 24)  #__init__(self,group,groupCount,groupRent,cost,baseRent,mortgage,*args):
        def test_initialization(self):
            self.site.changeOwner(self.banker)
            self.assertTrue(all([self.site.name=='mumbai',self.site.owner.name=='banker',self.site.rent==0]),msg='%s,arguments not reflecting'%self.site.owner.name)
        def test_execute(self):
            pass #ToDo
        def test_updateRent(self):
            self.site.changeOwner(self.banker)
            self.site.updateRent()
            self.assertTrue(all([self.site.rent==0,self.site.owner.name=='banker']),msg='arguments not reflecting')
            self.site.changeOwner(self.player1)
            self.site.updateRent()
            self.assertTrue(all([self.site.rent==0,self.site.owner.name=='vivek']),msg='arguments not reflecting')
            self.player1.completeSites.add(self.site)
            self.site.updateRent()
            self.assertTrue(all([self.site.rent==20,self.site.owner.name=='vivek']),msg='arguments not reflecting')

        def test_changeOwner(self):
            self.site= Site(123, 2, 20, 0, 0, 100, 'mumbai', self.banker, 24)  #__init__(self,group,groupCount,groupRent,cost,baseRent,mortgage,*args):
            self.site.changeOwner(self.player1)
            self.assertTrue(all([self.site.name=='mumbai',self.site.owner.name=='vivek',self.site.rent==0]),msg='arguments not reflecting')

    unittest.main()

