
import random
#import Brain
from Logger import Logger
from Participant import Participant
class Player(Participant):#args:position,turnCounter,name,cash,sites=[],purchase=[]
    def __init__(self, brain, **args):
        self.turn=0
        self.position=0
        self.completeSites=set([])
        self.mortgage={}
        self.purchase={'house':0,'hotel':0}
        rank=1
        self.brain=brain[0](self,*tuple(brain[1]))
        self.jailPass=0
        super(Player,self).__init__(**args)


    def changeSellingCost(self,site):
        """
        Will be implemented in future
        :param site:
        :return:
        """
        if site in self.sites:
            if site not in self.mortgage.keys():
                site.sellingCost=self.decision('sellingCost',site)

    def buySite(self, site):
        """
        connects with brain and buy/not buy on decision of brain
        :param site: Site
        :return:
        """
        if self.brain.buySite(site):
            if self.game.banker.siteMovement(self,site):return True
            else :
                print 'only way to buy is  mortgaging your sites, you require: '+str(site.sellingCost-self.cash)
                if self.mortgageChoice(site.sellingCost - self.cash): return self.buySite(site)
        return False


    def mortgagingAll(self):
        """
        give the max value earned by remaining site and all the site which are remaining
        :return: [int,[Site]]
        """
        totMortgage=0
        mortgagebleSites=[]
        for site in self.sites:
            if site not in self.mortgage:
                totMortgage += site.mortgage
                mortgagebleSites.append(site)

        return totMortgage,mortgagebleSites

    def obligation(self, receiver, amount):
        """
        receiver gets the amount and self have to pay , if not bankruptcy of player happens
        :param receiver: Participant
        :param amount: int
        :return: boolean
        """
        amountNeeded=amount-self.cash
        if amountNeeded<=0:self.transfer(receiver,amount)
        else:
            if amountNeeded>self.mortgagingAll()[0]:self.game.banker.bankruptcy(self,receiver,amount)
            else :
                while amountNeeded>0:
                    print "You have cash="+str(self.cash)+" .For clearing the payment please mortgage sites, you additionally need =" +str(amountNeeded)
                    Logger.info("Player doesnt have the cash so going for mortgage")
                    self.mortgageChoice(amountNeeded)
                    amountNeeded=amount-self.cash
                self.transfer(receiver,amount)
        return True




    #choices 1.buy the site  2. mortgage own sites  3.buy purchases
    def mortgageChoice(self, amountNeeded=0):
        """
        mortgages teh sites on nrain signal
        :param amountNeeded: int
        :return: boolean
        """
        mortAvailSites =self.mortgagingAll()
        if amountNeeded>mortAvailSites[0]:
            print "You can't no way get the desired amount from mortgaging so exiting mortgaging utility"
        else:
            amountEarned=0
            toMortgage=self.brain.mortgage(sites=mortAvailSites[1],amount=amountNeeded)
            for site in toMortgage:
                self.mortgageSite(site)
                amountEarned+=site.mortgage
                Logger.info("Player mortgaged :"+str(site.name))
            if amountEarned>=amountNeeded:return True
        return False



    def mortgageSite(self, site):
        """
        mortgages the site
        :param site: Site
        :return: boolean
        """
        if site in self.sites:
            if site not in self.mortgage.keys():
                self.game.banker.mortgage(site)
                return True
        return False

    def buyPurchase(self, site, purchase=1):
        """
        add specified purchases to site depending of brain signal and cash availabiity
        :param site: Site
        :param purchase: Purchase
        :return: boolean
        """
        min = site.purchase + 1
        if purchase>5-site.purchase:max=5
        else: max=purchase+site.purchase
        if site in self.completeSites and str(site.__class__.__name__)=='CitiSite':
            oldPurch=site.purchase
            for purchas in range(min,max):
                if purchas<4:
                    if self.transfer(self.game.banker,site.purchaseCost[0]):
                        if site.addPurchase():self.purchase['house']+=1
                    else:
                        print "Insuficient fund:only "+str(purchas)+"could be added.Your total Purchase for this site is "+str(site.purchase)
                        print 'Try mortgages,you still need the amount'+str((purchase-purchas)*site.purchaseCost[0])
                        if purchase<5:
                            if self.mortgageChoice((purchase-purchas)*site.purchaseCost[0]): self.buyPurchase(site,purchase-purchas)
                        else:
                            if self.mortgageChoice((purchase-1-purchas)*site.purchaseCost[0]+site.purchaseCost[1]):self.buyPurchase(site,purchase-purchas)
                        break
                elif purchas==5 :
                    if all([site.purchase==4 for site in self.game.banker.groupCompletness(self,site)]):
                        if self.transfer(self.game.banker,site.PurchaseCost[1]):
                            if site.addPurchase():self.purchase['hotel']+=1
                        else: print "Insuficient fund:only "+str(purchas)+" could be added.Your total Purchase for this site is "+str(site.purchase)
                        print 'Try mortgages,you still need the amount' + str( site.purchaseCost[1])
                        if self.mortgageChoice( site.purchaseCost[1]-self.cash):
                            self.buyPurchase(site,1)
                            break
                    else:
                        print 'check if all other complete sites in this grouup should have 4 purchases'

        else: print "Either site is not complete or this is not a citi site"

        return oldPurch<>site.purchase



    def payMortgage(self, site):
        """
        unmortgae the site by pauing 1.4* mortgage amount
        :param site: Site
        :return: boolean
        """
        if self.game.banker.unMortgage(site):
            return True
        else:
            print 'Not enough cash,Try mortgage to pay mortgage for site:'+str(site.name)
            if self.mortgageChoice(site.mortgage*1.4-self.cash): return self.payMortgage(site)
        return False
    def getWorth(self):
        """
        calculate total property cost + cash of the player
        :return: worth of the player
        """
        worth=self.cash
        for site in self.sites:
            worth+=site.cost
            if site.group[0]>100:
                    worth+=site.purchase*site.purchaseCost[0]
                    if site.purchase==5:
                        worth-=site.purchaseCost[0]+site.purchaseCost[1]
        for site in self.mortgage.keys():
            worth-=site.mortgage

        self.worth=worth
    def turnCounter(self):
        self.turn+=1
        sitesForPurchase=[]
        for site in self.completeSites:
            if str(site.__class__.__name__)=='CitiSite' :
                if site not in self.mortgage.keys() and site.purchase<5:sitesForPurchase.append(site)
        if len(sitesForPurchase)>0 :
            for site,pur in (self.brain.buyPurchase(sitesForPurchase)).items():
                self.buyPurchase(site,pur)
        if len(self.mortgage.keys())>0:
            for site in self.brain.payMortgage(self.mortgage.keys()):
                self.payMortgage(site)


    def jailChoice(self,jailFees):
        if self.brain.jail(jailFees):
            if self.transfer(self.game.banker,jailFees):return True
            else :
                print 'You dont have neccesary cash ,please mortgage to pay jail fees'
                if self.mortgageChoice(jailFees-self.cash):return self.jailChoice(jailFees)
        return False

    @staticmethod
    def dice():
        dice1=random.randrange(1,6)
        dice2=random.randrange(1,6)
        return dice1+dice2



if __name__ == '__main__':


    import unittest


    class TestPlayer(unittest.TestCase):
        from interfaces_test import player1,player2,banker,site1,site2,game
        def test_initialization(self):
            player10= Player(0, turnCounter=23, cash=100)
            if not self.assertTrue(all([player10.name=='vivek',player10.cash==100,player10.sites==[]]),msg='name is not reflecting'):self.fail

        def test_buySite(self):
            self.player1.cash=250
            self.player1.site=[]
            self.site1.owner=self.game.banker
            self.player1.buySite(self.site1)
            self.assertTrue(all([self.player1.sites==[self.site1],self.player1.cash==150]))

        def test_obligation(self):
            self.player1.cash=200
            self.site1.owner=self.player1
            self.site2.owner=self.player1
            self.player1.sites=[self.site1,self.site2]
            self.player1.mortgage={}
            self.player1.obligation(120, self.game.banker)
            self.assertTrue(self.player1.cash==80)
            self.player1.obligation(100, self.game.banker)  #both site mortgage would be chhosen
            self.assertTrue(self.player1.cash==60-20)
            self.player1.obligation(120, self.game.banker)
            self.assertTrue(self.game.players==[self.player2])


        def test_mortgageChoice(self):
            self.player1.cash=100
            self.player1.sites=[self.site1,self.site2]
            self.site1.owner=self.player1
            self.site2.owner=self.player1
            self.player1.mortgage={}

            self.player1.mortgageChoice(40)  #mortgaging both sites will be done
            self.assertTrue(all([self.player1.cash==160,self.player1.mortgage=={self.site1:0,self.site2:0}]))


        def test_payRent(self):
            self.site2.owner=self.player2
            self.player1.cash=100
            self.player2.cash=100
            self.player1.payRent(self.site2)
            self.assertTrue(all([self.player1.cash==90,self.player2.cash==110]))


        def test_buyPurchase(self):
            self.player1.cash=110
            self.player1.completeSites=[self.site1]
            self.player1.buyPurchase(self.site1, 3)
            self.assertTrue(all([self.site1.purchase==2,self.player1.cash==10]))
            self.player1.buyPurchase(self.site1, 1)
            self.assertTrue(all([self.site1.purchase==2,self.player1.cash==10]))




        def test_mortgage(self):
            pass # trivial main part will be tested in banker unittesting

        def test_payMortgage(self):
            pass#trivial, main parts lies in banker module

        def test_dice(self):
            pass#trivialle

    unittest.main()


