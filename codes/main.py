
import random,itertools
from Banker import Banker
from Player import Player
from Game import Game
from Logger import Logger
import Brain
import threading
import Queue
from multiprocessing import Pool,Process,cpu_count,Manager
import xlwt,copy

import time,sys,os
f = open(os.devnull, 'w')
old_stdout=sys.stdout
sys.stdout = f


def initiliazeParticipants(cashPerHead,playerName,game):
    numPlayer=len(playerName)
    banker= Banker(name="Banker", cash=numPlayer * cashPerHead * 10, game=game)
    players=[]
    for i in range(0,numPlayer):
        players.append(Player((Brain.pureRandom,[game]),name=playerName[i], cash=cashPerHead, game=game))
    return banker,players
def gameOn(x=None,game=None):
    if x is not None:
        gamer=''
        for brain in x:
            gamer+=str(brain)+','
        Logger.critical("Game Started:"+gamer)
    if game is None:
        nameSet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
        game=Game()
        i=0
        playerList=[]
        for player in x:
            playerList.append(nameSet[i])
            i+=1

        game.banker,game.players=initiliazeParticipants(2000,playerList,game)
        game.makeLuckSet("D:\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business")
        game.makeBoard('D:\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business')
        for i in range(len(x)):
            game.players[i].brain=x[i](game.players[i],game)
        game.players=game.playerTurnOrder(game.players)
    i=0
    turncounter=0
    ww1=xlwt.Workbook()
    ww1.add_sheet("turnsRecords",cell_overwrite_ok=True)
    sq=ww1.get_sheet(0)

    row=0
    sq.write(row , 0, 'name')
    sq.write(row , 1, 'position')
    sq.write(row , 2, 'cash')
    sq.write(row , 3, 'sites')
    sq.write(row , 4, 'mortgage')
    sq.write(row , 5, 'completeSites')
    sq.write(row , 6, 'inJail')
    row+=1

    while len(game.players)>1:
        turncounter+=1
        j = 0
        Logger.info('\n\n' + str(turncounter))
        if game.turnCounter(game.players[i]):
            roll=game.players[i].dice()
            sq.write(row,1,str(turncounter))
            sq.write(row,2,str(game.players[i].name))
            sq.write(row, 3, str(roll))

            row+=1

            newPosition=+game.players[i].position+roll
            Logger.info('player='+str(game.players[i].name)+',currentPosition='+str(game.players[i].position)+',dice='+str(roll))
            if newPosition>39:newPosition=newPosition-39
            game.players[i].position=newPosition
            game.board[game.players[i].position].execute(game.players[i], roll)
            for player1 in game.players:
                sq.write(row + j, 0, str(player1.name))
                sq.write(row + j, 1, str(player1.position))
                sq.write(row+j, 2, player1.cash)
                s=''
                for site in player1.sites:
                    s+=site.name +','
                sq.write(row+j, 3, s)
                s=''
                for site in player1.mortgage.keys():
                    s+=site.name +','
                sq.write(row+j, 4, s)
                s=''
                for site in player1.completeSites:
                    s+=site.name +','
                sq.write(row + j, 5, s)
                s=''
                for player in game.jail.keys():
                    s+=player.name +','
                sq.write(row + j, 6, s)
                j+=1
        row+=j+2
        #ww.save("D:\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business\\writtenByVivek_"+str(x)+".xls")
        i+=1
        if i>=len(game.players):i=0
    Logger.info("Winner:"+str(game.players[0].name))
    if x is not None:Logger.critical('Game_Ended:' +gamer)
    print "Winner:"+str(game.players[0].name)
    return game.players[0].name,turncounter



no_result=0
turns=0
import xlwt

ww = xlwt.Workbook()
ww.add_sheet("turnsRecords", cell_overwrite_ok=True)
sq = ww.get_sheet(0)

returnList = []
def simulator(n,x=None,game=None):
    dict={}
    turns=0
    if game is None:
        nameSet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
        for brain in range(len(x)):
            dict[nameSet[brain]]=[str(x[brain]),0]
    else:
        for player in game.players:
            dict[player.name]=[str(player.brain),0]

    for i in range(0,n):
        if game is not None:temp=copy.deepcopy(game)
        else: temp=None
        d=gameOn(x=x,game=temp)
        turns+=d[1]
        dict[d[0]][1]+=1
    return (dict,float(turns/n))

def jugad(que,n,x):
    que.put(simulator(n,x))


def main(thread=False,multiProcess=False,n=100,brains=[]):
    start_time = time.time()
    que=Queue.Queue()
    for brain in range(len(brains)):
        sq.write(0, brain, str(brains[brain]))
    az1=[]
    wholeCombin=itertools.combinations_with_replacement(brains,len(brains))
    counter=0
    if multiProcess:
        que=Manager().Queue()
        pool=Pool(processes=cpu_count())
    for x in wholeCombin:
                        if thread or multiProcess:
                            if thread:
                                a=threading.Thread(target=jugad,args=(que,n,x))
                                a.start()
                                az1.append(a)
                            else:pool.apply_async(jugad,args=(que,n,x))
                        else:jugad(que,n,x)
                        counter+=1
    if thread :
        for z in az1:z.join()
    elif multiProcess:
        pool.close()
        pool.join()
    row=1
    for element in range(counter):
            temp=que.get()
            sq.write(row*2,0,temp[1])
            j=1
            for key in temp[0].keys():
                sq.write(row*2,j,temp[0][key][0])
                sq.write(row*2+1,j,temp[0][key][1])
                j+=1
            row+=1
    timeTaken=time.time() - start_time
    sq.write(0, 6, str(timeTaken))
    sys.stdout = old_stdout
    print timeTaken


    ww.save("D:\Users\\703145584.INDGE\\Documents\\Genpact_Internal\\adhoc\\business\\writtenByVivek.xls")
if __name__ == "__main__":
    #brains=[Brain.pureRandom,Brain.averseRandom,Brain.groupMaker,Brain.aversegroupMaker2,Brain.futureSimulator]
    brains=[Brain.futureSimulator,Brain.aversegroupMaker2,Brain.groupMaker,Brain.pureRandom]
    x1=10
    #sys.stdout = f
    #main(n=x1,brains=brains)
    #sys.stdout = f
    #main(thread=True,n=x1,brains=brains)
    sys.stdout = f
    main(multiProcess=True,n=x1,brains=brains)

