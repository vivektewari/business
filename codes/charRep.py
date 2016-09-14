

from random import randint
from Card import Card
from Logger import Logger
class LuckCardHolder(Card):
    def __init__(self,cardSet,*args):
            self.cardSet=cardSet
            super(LuckCardHolder,self).__init__(*args)

    def execute(self, player, dice=0):
        self.cardSet[randint(0, len(self.cardSet) - 1)].execute(player, dice=0)








class ChaRep(object):
    def __init__(self,gotoPosition,yourMoney,theirMoney,jail,house,hotel,msg,number,game):
        self.gotoPosition=gotoPosition
        self.yourMoney=yourMoney
        self.theirMoney=theirMoney
        self.house=house
        self.jail=jail
        self.hotel=hotel
        self.msg=msg
        self.number=number
        self.game=game
    def calcAmount(self,game,player):
        temp=self.__dict__
        for key,value in temp.items():
            if value=='N/A':
                if key<>'gotoPosition':temp[key]=0
        return self.yourMoney-self.theirMoney*(len(game.players)-1)-player.purchase['house']*self.house-player.purchase['hotel']*self.hotel
    def execute(self, player, dice=0):
        print self.msg
        Logger.info(str(self.msg))
        amount=self.calcAmount(self.game, player)
        if amount<0:
            player.obligation(self.game.banker,-amount)
        else :self.game.banker.transfer(player,amount)
        for player1 in self.game.players:
            if player1 <> player:
                if self.theirMoney>0 :self.game.banker.transfer(player1,self.theirMoney)
                else :
                    player1.obligation(self.game.banker,-self.theirMoney)
        if self.gotoPosition<>'N/A':
            if not isinstance(self.gotoPosition,int ):
                minimum=40
                post=map(int,str(self.gotoPosition).split(','))
                for pos in post:
                    if abs(pos-player.position)<minimum:
                        minimum=abs(pos-player.position)
                        position=pos

            elif float(self.gotoPosition)%1<>0:
                position=player.position+int(self.gotoPosition)
                if position<0: position=40+position
            else :position=int(self.gotoPosition)
            self.goTo( player,position, self.game,dice)
        if amount <> 0:
            Logger.info("transferred to player="+str(amount)+" transferred to other player="+str(self.theirMoney))
        if self.jail==-1:player.jailPass+=1
        return True





    @staticmethod
    def goTo(player,position,game,dice):
        Logger.info("player to go to position="+str(position))
        player.position=position
        game.board[position].execute(player, dice)






if __name__ == '__main__':
    import unittest
    from xlrd import open_workbook
    from Game import Game


    class TestChaRep(unittest.TestCase):

        def test_calcAmount(self):
            wrkBook=open_workbook('D:\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business\\business_excel.xlsx')
            sheet=wrkBook.sheet_by_name('luckCard')
            row=1
            column=1
            luckcard=ChaRep.makeSet("D:\Users\\703145584\\Documents\\Genpact_Internal\\adhoc\\business")
            class game():
                players=[1,2,3,4]
            class player():
                purchase={'house':2,'hotel':3}

            for loop1 in luckcard:
                for loop2 in loop1:
                    while sheet.cell(row,column).value not in ('Community Chest','Chance') :row+=1
                    t=loop2.calcAmount(game,player),sheet.cell(row,19).value
                    self.assertTrue(loop2.calcAmount(game,player)==sheet.cell(row,19).value)
                    row+=1

        def test_execute(self):
            #depends on other classes
            pass

        def test_goTo(self):
            #trivial
            pass













    unittest.main()

