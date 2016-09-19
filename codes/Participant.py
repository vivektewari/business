
import abc
class Participant(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, cash,game):
        """

        :param game:
        :param name: string
        :param cash: int
        :param sites:list[site]
        :param purchase:int
        :return:Participant
        """
        self.name=name
        self.initialMoney=cash
        self.cash=cash
        self.sites=[]
        self.worth=self.cash
        self.game=game



    def transfer(self,anotherParticipant,amount):
        if amount>0 and self.cash-amount>=0:
            self.__changeAmount(-amount)
            anotherParticipant.__changeAmount(amount)
            return True
        elif amount<0:raise ValueError("amount can only be positive")
        else:
            print "Payment unsucessful:Not enough cash"
            return  False
    def __changeAmount(self,amount):
        self.cash+=amount
        self.worth+=amount

    def groupCompletness(self,site):
        """
        checks for group completion
        :param site: Site
        :return:the whole group of site  if a  particular site completes the group
        """
        if site.owner==self:match=0
        else:match=1
        siteList=[]
        for sites1 in self.sites:
            if sites1.group[0]==site.group[0]:
                match+=1
                siteList.append(sites1)
        if match>=site.group[1]:
            return siteList
        else: return []


    @staticmethod
    def disabledmethods():
        raise Exception('Function Disabled')

if __name__ == '__main__':
    import unittest


    class TestParticipant(unittest.TestCase):

        player= Participant('name', 100, False)
        player2= Participant('tester', 100, False)
        def test_initialization(self):
            self.assertTrue(all([self.player.name=='name',self.player.cash==100]),msg='arguments not reflecting')

        def test_transfer(self):
            self.player.transfer(self.player2,200)
            self.assertTrue(all([self.player.cash==100,self.player2.cash==100]),msg='arguments not reflecting')
            self.player.transfer(self.player2,20)
            self.assertTrue(all([self.player.cash==80,self.player2.cash==120,self.player.worth==80]),msg='arguments not reflecting')




        def test_groupCompletness(self):
            from Site import Site
            class site1:
                group=(1,2,3)
            class site2:
                group=(1,3,4)

            self.player.sites.append(site1)
            completedSites1=self.player.groupCompletness(site1)
            self.player.sites.append(site2)
            completedSites2=self.player.groupCompletness(site1)
            completedSites3=self.player.groupCompletness(site2)
            self.player.sites.remove(site2)
            completedSites4=self.player.groupCompletness(site1)
            self.assertTrue(all([completedSites1==[],completedSites3==[],completedSites4==[],completedSites2==[site1,site2]]))

        def test_disabledmethods(self):
            pass #not required to test
        def test_getWorth(self):
            pass #tested in test_transfer

    unittest.main()






