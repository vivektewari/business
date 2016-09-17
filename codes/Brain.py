
from abc import ABCMeta,abstractmethod
from main import simulator
import random,copy
from Logger import Logger
class Brain(object):
    __metaclass__ = ABCMeta
    decisionCodes={'buySite','buyPurchase','mortgage','payMortgage','jail'}
    description=""
    def __init__(self,player,game):
        self.player=player
        self.game=game
    @abstractmethod
    def buySite(self):pass
    @abstractmethod
    def buyPurchase(self,sitePos):pass
    @abstractmethod
    def mortgage(self,sitePos):pass# required in buying site or purchase or obligation or getting out of jail
    @abstractmethod
    def jail(self,jailFees):pass
    @abstractmethod
    def payMortgage(self,sites):pass
class pureRandom(Brain):
    description='Purely random decision without considering anything'
    def randomSelection(self,sites):
        siteList=[]
        for site in sites:
            if bool(random.randint(0,1)):siteList.append(site)
        return siteList
    def buySite(self,site):
        return bool(random.randint(0, 1))
    def mortgage(self,sites,amount):
        return self.randomSelection(sites)
    def payMortgage(self,sites):
        return self.randomSelection(sites)
    def buyPurchase(self,sites):
        final={}
        selected=self.randomSelection(sites)
        for site in selected:final[site]=random.randint(0,6)
        return final
    def jail(self,jailFees):
        return bool(random.randint(0, 1))
class averseRandom(pureRandom):
    description = "behave purely like random just never go for mortrtgage other than it is obligation"

    def buyPurchase(self,sites):
        cash=self.player.cash
        final={}
        for site in sites:
            if site.purchase<4:
                cash-=site.purchaseCost[0]
            elif site.purchase==4:
                cash-=site.purchaseCost[1]
            if cash>0:
                if site in final.keys():final[site]+=1
                else:final[site]=1
        return final


    def payMortgage(self,sites):
        final=[]
        cash=self.player.cash
        for site in self.randomSelection(sites):
            cash-=int(site.mortgage*1.4)
            if cash>0:final.append(site)
            else:break
        return final

    def jail(self,jailFees):
        if self.player.cash>=jailFees: return bool(random.randint(0, 1))
        return False
    def buySite(self,site):
        if self.player.cash>=site.sellingCost:return bool(random.randint(0, 1))
        return False
class groupMaker(averseRandom):
    description = "Not random ,if have money then only perform task ,if dont have money and site making group ,its buys it"
    def priorityOrder(self,sites):
        req1=[]
        rest=[]
        complete=[]
        for site in sites:
            match=0
            for site1 in sites:
                if site.group[0]==site1.group[0]:match+=1
            if site.group[1]<=match:complete.append(site)
            elif site.group[1]-match==1:req1.append(site)
            else: rest.append(site)
        complete=sorted(complete,key=lambda x:x.rent)
        return rest+req1+complete
    def buySite(self,site):
        if self.player.cash>=site.sellingCost:return True
        elif self.player.groupCompletness(site) <> []:return True
        return False
    def mortgage(self,sites,amount):
        amountCollected=0
        final=[]
        for site in self.priorityOrder(sites):
            amountCollected+=site.mortgage
            final.append(site)
            if amountCollected>=amount:break
        return final
    def payMortgage(self,sites):
        final=[]
        cash=self.player.cash
        for site in self.priorityOrder(sites):
            cash-=int(site.mortgage*1.4)
            if cash>0:final.append(site)
            else:break
        return final
class aversegroupMaker2(groupMaker):
    description='keep out some out of 100 cash for security in future.Also once cash is less only buy the sites for which group can be made'
    def siteToBuy(self):
        required=0
        for site in self.game.banker.sites:
            if len(self.player.groupCompletness(site))>1:required+=1
        return required

    def buySite(self,site):
        if self.player.groupCompletness(site) <> [] and site.sellingCost-self.player.cash<50:return True
        if self.siteToBuy()>1 and self.player.cash<150 and self.player.groupCompletness(site) == []:return False
        elif self.player.cash - 100 >= site.sellingCost:return True
        return False
    def jail(self,jailFees):
        if self.player.cash>=jailFees-100 :
            if (self.player.cash/float(self.player.initialMoney))>0.5 or self.siteToBuy()>1: return True
        return False
class futureSimulator(aversegroupMaker2):

    def __init__(self,player,game,numSimulation=100,simulate=True):
        self.simulate=simulate
        self.caser=-1
        self.numSimulation=numSimulation
        super(futureSimulator,self).__init__(player,game)
        self.index=-1
    def simulTree(self,game):
                for player in game.players:
                    if str(player.brain.__class__.__name__)=='futureSimulator':
                        player.brain.simulate=False
                        player.brain.caser=-1
                playerOrdering=game.players[self.index+1:]+game.players[0:self.index+1]
                game.players=playerOrdering
                return simulator(n=self.numSimulation,game=game)[0][self.player.name][1]

    def selfIndex(self,game):
        i=0
        for player in game.players:
            if player.name==self.player.name:self.index=i
            i+=1




    def buySite(self,site):
        if self.simulate:
            result={}
            for i in range(2):
                game=copy.deepcopy(self.game)
                self.selfIndex(game)
                game.players[self.index].brain.caser=i
                game.players[self.index].brain.simulate=False
                for site1 in game.board:
                    if site1.name==site.name:
                        game.players[self.index].buySite(site1)
                        break
                result[i]=self.simulTree(game)
            #if super(futureSimulator,self).buySite(site)<>result[0]>=result[1]:Logger.critical(str(self.player.cash)+','+str( result[0])+','+str(result[1] ))
            if result[0]>=result[1] :return True
            else :return False
        else:
            if self.caser==0 :return True
            elif self.caser==1:return False
            else :return super(futureSimulator,self).buySite(site)
    def jail(self,jailFees):
        if self.simulate:
            result={}
            for i in range(2):
                game=copy.deepcopy(self.game)
                self.selfIndex(game)
                game.players[self.index].brain.caser=i
                game.players[self.index].brain.simulate=False
                game.players[self.index].jailChoice(jailFees)
                result[i]=self.simulTree(game)
            if result[0]>=result[1] :return True
            else:return False
        else:
            if self.caser==0 :return True
            elif self.caser==1:return False
            else :return super(futureSimulator,self).jail(jailFees)
    def buyPurchase(self,sites):
        if self.simulate:
            final={}
            result={}
            for site in sites:
                for i in range(2):
                    game = copy.deepcopy(self.game)
                    self.selfIndex(game)
                    game.players[self.index].brain.simulate = False
                    if i==0:
                        for site1 in game.players[self.index].completeSites:
                            if site1.name==site.name and game.players[self.index].cash>=site1.purchaseCost[1]:
                                game.players[self.index].buyPurchase(site1,1)
                                break
                            result[i]=self.simulTree(game)
                        if result[0]>=result[1]:final[site]=1
            return final
        else:return super(futureSimulator,self).buyPurchase(sites)




















class manual(Brain):
    def __init__(self,player,game):

        description='manual choices in runtime'
    def buySite(self,site):
       if int(raw_input("Choose 1 if you want to buy the site ,else press any other key and pay the rent to the banker .Site :"+str(site.name)))==1:return True
       return False
    def mortgage(self,sitePos,amount):
        """
        :param sitePos:
        :param amount:
        :return:
        """
        print "Press 1 if you want to go ahead with mortgage to collect amount, else press any other key .Amount you need: "+ str(amount)
        if int(raw_input())==1:
            required=amount
            while required>0:
                toMortgage = []
                print "amount you more require:"+str(required)
                try:
                    for site in sitePos:
                            print site.name, site.position, site.mortgage
                    askMortgage = raw_input("Please key in the site positions you want to mortgage seperated by comma, If want to exit press -1 .Your required amount is:"+str(required))
                    input = list(map(int, askMortgage.split(",")))
                    if input==[-1]:
                        return []
                    else:
                        for site in sitePos:
                            if site.position in input :
                                required -= site.mortgage
                                toMortgage.append(site)
                        if required<amount:
                            print "You further require: "+str(required)+" press 1 if you want to go ahead with selected mortgages else press any other key to start from begning"
                            if int(raw_input())==1:return toMortgage

                except:print 'invalid inputs,please try again'
                return toMortgage
        return False
    def payMortgage(self,site):
        if int(raw_input("Choose 1 to pay the mortgage .Site,unmortgage payment:" + str(site.name)+','+str(int(1.4*site.mortgage)))) == 1: return True
        return False


    def buyPurchase(self,sites):
        final={}
        for site in sites:
            print site.name,site.position,site.purchase,site.purchaseCost
            choice=raw_input('please key in number of extra purchases you want for this ,or press any other number if not interested in extra purchases')
            try:
                if int(choice) in [1,2,3,4,5]:final[site]=choice
            except:pass
        return final




    def jail(self,jailFees):
        try:return int(raw_input("Choose 1 if you want to pay the jail fees and get free next turn.Jail fees is  :"+str(jailFees)))==1
        except:pass
        return False









