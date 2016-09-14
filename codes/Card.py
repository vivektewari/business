

import abc
class Card(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self,name,position,game):
        """

        :param name: str
        :param owner: Participant
        :param position: int
        :return: Card
        """
        self.name=name
        self.game=game
        self.owner=game.banker
        self.position=position

    @abc.abstractmethod
    def execute(self, player, dice=0):pass

if __name__ == '__main__':
    from unittest import TestCase
    import unittest


    class TestCard(TestCase):
        card=Card('vivek','ret',21)
        def test_execute(self):
            pass #function just for abstraction
        def test_initilization(self):
            self.assertTrue(all([self.card.name=='vivek',self.card.owner=='ret',self.card.position==21]),msg='arguments not reflecting')
    unittest.main()
