
from Site import Site
import logging

class UtilitySite(Site):


    def execute(self, player, dice=0):
        oldRent=self.rent
        self.rent= self.rent * dice
        logging.info("player landed to utility  site and depending upon his dice rent is="+str(self.rent))
        super(UtilitySite, self).execute(player, dice)
        self.rent=oldRent
        return True


if __name__=='__main__':
    import unittest
    class TestUtilitySite(unittest.TestCase):pass#manually tested because of function nature
    pass


    unittest.main()





