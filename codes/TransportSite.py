
from Site import Site
from Logger import Logger
class TransportSite(Site):
    def updateRent(self):
        match=1
        oldRent=self.rent
        if str(self.owner.__class__.__name__=='Player'):
            for site in self.owner.completeSites:
                if site.group[0]==self.group[0] and site<>self:
                    match+=1
            self.rent=match*self.baseRent
            if self.rent<>oldRent:Logger.info('rent update to:'+str(self.rent))
        return self.rent<>oldRent

if __name__=='__main__':
    import unittest
    class TestTransportSite(unittest.TestCase):
        class Banker(object):pass
        banker=Banker()
        banker.name='banker'
        class Player(object):pass
        player=Player()
        player.name='vivek'
        player.completeSites=set([])
        transportSite2= TransportSite(123, 2, 10, 10, 10, 100, 'mumbai', banker, 24)
        transportSite= TransportSite(123, 2, 10, 10, 10, 100, 'mumbai', banker, 24)  #__init__(self,group,groupCount,groupRent,cost,baseRent,mortgage,*args):
        def test_updateRent(self):
            self.transportSite.changeOwner(self.banker)
            self.transportSite.updateRent()
            self.assertTrue(all([self.transportSite.rent==10,self.transportSite.owner.name=='banker']),msg='arguments not reflecting')
            self.transportSite.changeOwner(self.player)
            self.transportSite.updateRent()
            self.assertTrue(all([self.transportSite.rent==10,self.transportSite.owner.name=='vivek']),msg='arguments not reflecting')
            self.player.completeSites.add(self.transportSite)
            self.transportSite.updateRent()
            self.assertTrue(all([self.transportSite.rent==10,self.transportSite.owner.name=='vivek']),msg='arguments not reflecting')
            self.player.completeSites.add(self.transportSite2)
            self.transportSite.updateRent()
            self.assertTrue(all([self.transportSite.rent==20,self.transportSite.owner.name=='vivek']),msg='arguments not reflecting')
    unittest.main()


