from Participant import Participant
from Logger import Logger


class Banker(Participant):  # arguments order->name,cash
    def __init__(self, **args):
        super(Banker, self).__init__(**args)

    def mortgageCounter(self, player):
        """
        increased the mortgage tenure by 1 unit
        :param player: Player
        :return: boolean
        """
        if len(player.mortgage.keys()) > 0:
            for site in player.mortgage.keys():
                player.mortgage[site] += 1
                if player.mortgage[site] > 3:
                    self.siteMovement(self, site)
                    print site.name + ' has been taken as mortgage amount was not paid in 3 turns'
                    Logger.info(str(site.name) + ' has been taken as mortgage amount was not paid in 3 turns')
            return True
        return False

    def turnCounter(self, player):
        self.mortgageCounter(player)

    def mortgage(self, site):
        site.owner.mortgage[site] = 0
        self.transfer(site.owner, site.mortgage)
        site.owner.getWorth()
        return True

    def unMortgage(self, site):
        if site in site.owner.mortgage:
            if site.owner.transfer(self, int(site.mortgage * 1.4)):  # to unmortgage , 1.4 time needs to paid
                del site.owner.mortgage[site]
                Logger.info("site unmortgaged:" + str(site.name))
                return True
        return False

    def siteMovement(self, player2, site):
        """
        moves a particular site from a player1t to other player2 doing all the neccesary changes
        :param player: Participant
        :param site: Site
        :param outgoing: boolean
        :return: true if site transfer is sucessfull
        """
        go = False
        if player2 == self:
            go = True  # site movesto banker only through mortgages .
        elif player2.transfer(site.owner, site.sellingCost):
            go = True
        if go:
            player1 = site.owner
            site.changeOwner(player2)
            completeness = []
            if player1 <> self:
                completeness = set(player1.groupCompletness(site))
                completeness ^= set(player1.completeSites)
                player1.completeSites = list(completeness)
            if player2 <> self:
                if len(completeness) == 0:
                    completeness = set(player2.groupCompletness(site))
                    completeness =completeness | set(player2.completeSites)
                    player2.completeSites = list(completeness)
            for sites1 in completeness:
                if str(sites1.__class__.__name__) == 'CitiSite' and player1 <> self:
                    oldpurchase = sites1.purchase
                    if sites1.updateRent():
                        if oldpurchase < 5:
                            player1.purchase['house'] += (sites1.purchase - oldpurchase)
                        elif oldpurchase == 5:
                            player1.purchase['house'] += (sites1.purchase - oldpurchase - 1)
                            player1.purchase['hotel'] -= 1
                else:
                    sites1.updateRent()
            return True
        else:
            print "dont have enough cash to buy"
            return False

    def groupCompletness(self, site):
        self.disabledmethods()

    def bankruptcy(self, payee, receiver, amount):
        """
        player is removed from the game and all his property been taken by banker
        :param payee: Player
        :param receiver: Participant
        :param amount: int
        :return: boolean
        """
        self.transfer(receiver, amount)
        for site in self.sites:
            self.game.banker.siteMovement(self.game.banker, site)
        payee.transfer(self, payee.cash)
        self.game.players.remove(payee)
        if payee in self.game.jail.keys(): del self.game.jail[payee]
        Logger.info('Player removed due to bankruptcy:' + str(payee.name))
        return True


if __name__ == '__main__':
    from unittest import TestCase
    from Site import Site
    from Player import Player
    import unittest


    class TestBanker(TestCase):
        from interfaces_test import player1, player2, site1, site2

        # site1= Site(123, 25, 2, 100, 10, 50, '', 'mumbai', player,24)  #group,cost,baseRent,mortgage,choiceMsg,name,owner,position)
        # site2=Site(123,20,2,100,15,50,'','kolkata',player,23)#group,cost,baseRent,mortgage,choiceMsg,name,owner,position
        # site1.updateRent()
        # site2.updateRent()

        banker = Banker(name='banker', cash=100)

        def test_initialization(self):
            self.assertTrue(all([self.banker.name == 'banker', self.banker.cash == 100, self.banker.sites == []]),
                            msg='name is not reflecting')

        def test_mortgageCounter(self):
            self.site1.owner = self.player1
            self.player1.mortgage = {self.site1: 0}
            self.player1.sites = [self.site1, self.site2]
            self.banker.mortgageCounter(self.player1)
            self.banker.mortgageCounter(self.player1)
            self.assertTrue(self.player1.mortgage == {self.site1: 2})
            self.banker.mortgageCounter(self.player1)
            self.banker.mortgageCounter(self.player1)
            self.assertTrue(all([self.player1.mortgage == {}, self.player1.sites == [self.site2]]))

        def test_mortgage(self):
            self.player1.sites.append(self.site1)
            self.site1.owner = self.player1
            self.banker.mortgage(self.site1)

            self.assertTrue(all([self.player1.cash == 130, self.player1.mortgage == {self.site1: 0}]))

        def test_unMortgage(self):
            self.player1.sites = [self.site1]
            self.site1.owner = self.player1
            self.player1.cash = 90
            self.banker.mortgage(self.site1)
            self.assertTrue(all([self.player1.cash == 120, self.player1.mortgage == {self.site1: 0}]))
            self.banker.unMortgage(self.site1)
            self.assertTrue(all([self.player1.cash == 90, self.player1.mortgage == {}]))

        def test_groupCompletness(self):
            pass  # method disabled

        def test_siteMovement(self):
            self.player1.sites = [self.site1]
            self.player2.sites = []
            self.banker.siteMovement(self.player2, self.site1)
            self.assertTrue(
                all([self.site1.rent == 10, self.player2.sites == [self.site1], self.site1.owner == self.player2]))
            self.site2.owner = self.banker
            self.banker.sites = [self.site2]
            self.banker.siteMovement(self.player2, self.site2)
            self.assertTrue(all([self.site1.rent == 20, self.site2.rent == 30, self.player1.sites == []]))


    unittest.main()


