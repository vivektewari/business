
from Site import Site
from Logger import Logger
class CitiSite(Site):
    def __init__(self,houseCost,hotelCost,house1,house2,house3,house4,hotel, *args):#args:PurchaseCost,rentPurchase,group,cost,baseRent,mortgage,choiceMsg,name,owner,position
        """

        :param group1:
        :param PurchaseCost: int
        :param args: see Site
        :return: CitiSite
        """

        self.rentPurchase= [house1,house2,house3,house4,hotel]     #house and hotel rent are implemented by liste
        self.purchaseCost=[houseCost, hotelCost]       #house and hotel both implemented in purchase by list
        self.purchase=0
        super(CitiSite,self).__init__(*args)

    def addPurchase(self):
        """
        increases purchase variable by 1
        :return: True
        """
        oldPurchase=self.purchase
        if  self.purchase<len(self.rentPurchase):
            self.purchase+=1
            self.updateRent()
        if oldPurchase<>self.purchase: Logger.info("purchase added, new purchases  =" + str(self.purchase))
        return oldPurchase<>self.purchase



    def updateRent(self):
        oldRent=self.rent
        super(CitiSite,self).updateRent()
        if self.rent==self.baseRent:
            self.purchase=0
        elif self.purchase>0:
            self.rent=self.rentPurchase[self.purchase-1]
        if oldRent <> self.rent: Logger.info(str(self.name)+ " rent updated to =" + str(self.rent))
        return oldRent<>self.rent

if __name__ == '__main__':
    import unittest


    class TestCitiSite(unittest.TestCase):
        class player:
            name='vivek'
            completeSites=set([])
        site= CitiSite(100, 0, 0, 100, 150, 250, 350, 123, 2, 20, 10, 10, 100, 'mumbai', player, 24)  #PurchaseCost,rentPurchase,group,cost,baseRent,mortgage,choiceMsg,name,owner,position
        def test_initialization(self):
            self.assertTrue(all([self.site.name=='mumbai',self.site.owner.name=='vivek',self.site.rent==10]))
        def test_addPurchase(self):
            for y in range(3):
                if y==0: pass
                elif y==1 :self.player.completeSites.add(self.site)
                else:self.player.completeSites.remove(self.site)
                self.site.updateRent()
                for i in range(0,10):
                    returnValue=self.site.addPurchase()
                    if returnValue:self.assertTrue(all([self.site.rent==self.site.rentPurchase[i], self.site.purchase==i+1]),msg='%d arguments not reflecting' %i)
                    else:
                        if y<>1:self.assertTrue(all([self.site.rent==10, self.site.purchase==0]),msg='%d,%d arguments not reflecting' %(y,i))
                        elif i<4 :self.fail()
        def test_updateRent(self):
            for y in range(3):
                if y==0: self.assertTrue(all([self.site.rent==10, self.site.purchase==0]),msg='%d, arguments not reflecting' %(y))
                elif y==1:
                    self.player.completeSites.add(self.site)
                    self.site.updateRent()
                    self.assertTrue(all([self.site.rent==20, self.site.purchase==0]),msg='%d, arguments not reflecting' %(y))
                else:
                    self.player.completeSites.remove(self.site)
                    self.site.updateRent()
                    self.assertTrue(all([self.site.rent==10, self.site.purchase==0]),msg='%d, arguments not reflecting' %(y))








    unittest.main()

