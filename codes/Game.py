
from random import randint
from xlrd import open_workbook
class Game(object):
    def __init__(self,players=[],banker=[]):#initialization with players list,banker
        self.board=[]
        self.players=players
        self.banker=banker
        self.jail={}


    def playerTurnOrder(self,players):
        finalOutput=[]
        initial=players
        ranks={}
        diced=[]

        for player in initial:
            dice=player.dice()
            diced.append((dice,player))
            rank=1
            for player1 in ranks.keys():
                if dice<ranks[player1][1]:rank+=1
                elif dice>ranks[player1][1]:ranks[player1][0]+=1
            ranks[player]=[rank,dice]
        rankDictionary={}
        for  player in ranks.keys():
            if ranks[player][0] in rankDictionary.keys():
                rankDictionary[ranks[player][0]].append(player)
            else:  rankDictionary[ranks[player][0]]=[player]
        for rank in rankDictionary.keys():
            if len(rankDictionary[rank])>1:
                finalOutput.extend(self.playerTurnOrder(rankDictionary[rank]))
            else:finalOutput.append(rankDictionary[rank][0])

        return finalOutput

    def executePosition(self,player,card,role=0):
        card.execute(player, role)
    @staticmethod
    def populate(sheet,row,*args):
        arguments=[]
        for element in args:
            if isinstance(element,int):
                if isinstance(sheet.cell(row,element).value,float):arguments.append(int(sheet.cell(row,element).value))
                else :arguments.append(sheet.cell(row,element).value)
            else:arguments.append(element)
        return tuple(arguments)

    def makeLuckSet(self,location):
        from xlrd import open_workbook
        from chaRep import ChaRep
        wrkBook=open_workbook(str(location+'\\business_excel.xlsx'))
        chance=[]
        community=[]
        sheet=wrkBook.sheet_by_name('luckCard')
        for row in range(0,100):
            argList=self.populate(sheet,row,3,4,5,6,7,8,2,0,self)
            if sheet.cell(row,1).value=='Community Chest':community.append(ChaRep(*argList))
            elif sheet.cell(row,1).value=='Chance':chance.append(ChaRep(*argList))
            elif sheet.cell(row,1).value=='STOP':break
        return community,chance


    def makeBoard(self,location):
        from chaRep import LuckCardHolder
        from interfaces_test import InterfaceError
        from TransportSite import TransportSite
        from CitiSite import CitiSite
        from UtilitySite import UtilitySite
        from CornerCard import CornerCard
        from Tax import Tax
        from Jail import Jail
        community,chance=self.makeLuckSet(location)
        wrkBook=open_workbook(str(location+'\\business_excel.xlsx'))
        sheet=wrkBook.sheet_by_name('board')
        board=[]
#input excel col_sequence={position:0,'group':1,'groupCount':2,'groupRent':3,'name':4,cost':5,'baseRent':6,'mortgage':7,'houseCost':8,'hotelCost':9,'house1':10,'house2':11,'house3':12,'house4':13;'hotel':14}#Color groupMember	#	Name	Cost/toReceive	Rent mortgage House Cost	Hotel Cost	1	2	3	4		houses	hotels
        for row in range(0,100):
            if sheet.cell(row,1).value=='STOP':break
            elif sheet.cell(row,0).value not in range(0,50):continue
            elif sheet.cell(row,1).value>0:#sites
                if sheet.cell(row,1).value>100:#citisite:houseCost,hotelCost,house1,house2,house3,house4,hotel,group,groupCount,groupRent,cost,baseRent,mortgage,name,owner,position
                   board.append(CitiSite(*self.populate(sheet,row,8,9,10,11,12,13,14,1,2,3,5,6,7,4,0,self)))
                elif sheet.cell(row,1).value>10:#transportSite:group,groupCount,groupRent,cost,baseRent,mortgage,name,owner,position
                   board.append(TransportSite(*self.populate(sheet,row,1,2,3,5,6,7,4,0,self)))
                elif sheet.cell(row,1).value>0:#UtilitySite:group,groupCount,groupRent,cost,baseRent,mortgage,name,owner,position
                   board.append(UtilitySite(*self.populate(sheet,row,1,2,3,5,6,7,4,0,self)))
            elif sheet.cell(row,1).value>-10:#chance or community
                if sheet.cell(row,1).value==-1:board.append(LuckCardHolder(*self.populate(sheet,row,community,"Community Chest",0,self)))
                elif sheet.cell(row,1).value==-2:board.append(LuckCardHolder(*self.populate(sheet,row,chance,"Chance",0,self)))
                else: InterfaceError('community is -1 and chance is -2 . other groups fro them are not allowed')
            elif sheet.cell(row,1).value>-100:#tax cards
                board.append(Tax(*self.populate(sheet,row,5,6,8,9,4,0,self)))
            elif sheet.cell(row,1).value>-1000:#corner cards
                if  sheet.cell(row,1).value==-111:board.append(CornerCard(*self.populate(sheet,row,5,'False',4,0,self)))
                else:board.append(CornerCard(*self.populate(sheet,row,5,6,4,0,self)))
            elif sheet.cell(row,1).value>-10000:#jail
                board.append(Jail(*self.populate(sheet,row,5,4,0,self)))

            else:     InterfaceError('Not a valid group')
            if sheet.cell(row,1).value>0 :self.banker.sites.append(board[-1])
        self.board=board
    def jailUpdation(self,player):
        if player in self.jail.keys():
            self.jail[player]+=1
            if self.jail[player]>=3 :del self.jail[player]
            return True
        return False
    def turnCounter(self,player):
        self.banker.turnCounter(player)
        if player in self.jail.keys():
            self.jailUpdation(player)
        else:
            player.turnCounter()
            return True
        return False








if __name__ == '__main__':

    import unittest


    class TestGame(unittest.TestCase):
        banker='dummy'
        players=[1,2,3,4]
        game=Game(players,banker)

        def test_playerTurnOrder(self):
            pass #have random components , so has been tested in debug mode

        def test_roleDice(self):
            pass #to trivial so not tested

        def test_executePosition(self):
            self.fail()
        def test_makeLuckSet(self):
            wrkBook=open_workbook('D:\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business\\business_excel.xlsx')
            sheet=wrkBook.sheet_by_name('luckCard')
            row=1
            column=1
            luckcard=self.game.makeLuckSet("D:\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business")
            for loop1 in luckcard:
                for loop2 in loop1:
                    while sheet.cell(row,column).value not in ('Community Chest','Chance') :row+=1
                    #gotoPosition,yourMoney,theirMoney,jail,house,hotel,msg,number
                    self.assertTrue(all([loop2.gotoPosition==sheet.cell(row,3).value,loop2.yourMoney==sheet.cell(row,4).value,loop2.theirMoney==sheet.cell(row,5).value,loop2.jail==sheet.cell(row,6).value,loop2.house==sheet.cell(row,7).value,loop2.hotel==sheet.cell(row,8).value,loop2.msg==sheet.cell(row,2).value,loop2.number==sheet.cell(row,0).value]))
                    row+=1
        def test_populate(self) :
            wrkBook=open_workbook('D:\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business\\business_excel.xlsx')
            sheet=wrkBook.sheet_by_name('luckCard')
            tester=self.game.populate(sheet,8,0,1,2,3,4,5,6,7,8)
            self.assertTrue(tester==(6.0,'Community Chest',	'Go to Jail',	40.0,	'N/A',	'N/A',	'N/A',	'N/A',	'N/A'))



        def test_makeBoard(self):

            self.game.makeBoard('D:\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business')
            board=self.game.board
            testingSample=[0,2,4,9,35,39]
            self.assertTrue(all([board[0].amount==200,board[2].cardSet[2].theirMoney==-50,board[4].perHouse==20,board[9].mortgage==60,board[35].rent==20,board[39].rentPurchase==[200,600,1400,1700,2000]]))

    unittest.main()

