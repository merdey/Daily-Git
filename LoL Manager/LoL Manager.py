import pickle, math, sys, random
from player import *
from team import *
from league import *

GAME_DAY_ACTIONS = ['rest', 'play', 'train']
OFF_DAY_ACTIONS = ['rest', 'train', 'stream']
NORMAL_GAME_WINNINGS = 100

class Game:  
    def __init__(self):
        self.day = 27
        self.league = newLeague()
        self.player_team = self.league.teams[0]

    def nextDay(self):
        self.day += 1
        print('day: ' + str(self.day))

        #season playoffs
        if self.day % 28 == 0:
            print('Season Playoffs!')
            self.simPlayoffs()
        #game day
        elif self.day % 7 == 0:
            print('Game Day!')
            self.setGameDayActions()
                
            matchups = self.league.generateWeeklyMatchups()
            for mu in matchups:
                self.showGameResults(mu)
        #normal day
        else:
            for team in self.league.teams:
                if team == self.player_team:
                    team.setPlayerActions('human', OFF_DAY_ACTIONS)
                    team.takePlayerActions()
                else:
                    team.setPlayerActions('ai', OFF_DAY_ACTIONS)
                    team.takePlayerActions()

        for team in self.league.teams:
            team.collectStreamIncome()
            team.paySalaries()

    def showGameResults(self, mu):
        print( mu[0].name + ' ' + str(mu[0].record) + ' vs ' + mu[1].name + ' ' + str(mu[1].record) )
        result = self.simGame(mu)
        if result == 'tie':
            print('Tie Game')
        else:
            print(result + ' wins')

    def setGameDayActions(self):
        for team in self.league.teams:
            if team == self.player_team:
                team.setPlayerActions('human', GAME_DAY_ACTIONS)
                while not team.isGameReady():
                    print('Error: team must have exactly 5 players playing')
                    team.setPlayerActions('human', GAME_DAY_ACTIONS)
                team.takePlayerActions()
            else:
                while not team.isGameReady():
                    team.setPlayerActions('ai', GAME_DAY_ACTIONS)
                team.takePlayerActions()

    def simPlayoffs(self):
        seeds = self.league.generatePlayoffBracket()
        print(seeds)
        print(len(seeds))
        print(int(math.log(len(seeds), 2)) + 1)
        for round_number in range(1, int(math.log(len(seeds), 2)) + 1):
            print('round ' + str(round_number))
            self.setGameDayActions()
            
    def simGame(self, mu):
        blue_team = mu[0]
        blue_team_skill = 0
        for player in blue_team.players:
            blue_team_skill += (player.skill * player.stamina)
        randomFactor = random.random()
        blue_team_strength = blue_team_skill * randomFactor

        purple_team = mu[1]
        purple_team_skill = 0
        for player in purple_team.players:
            purple_team_skill += (player.skill * player.stamina)
        randomFactor = random.random()
        purple_team_strength = purple_team_skill * randomFactor

        if blue_team_strength > purple_team_strength:
            blue_team.record[0] += 1
            blue_team.money += NORMAL_GAME_WINNINGS
            purple_team.record[2] += 1
            return blue_team.name
        elif blue_team_strength == purple_team_strength:
            blue_team.record[1] += 1
            blue_team.money += int(NORMAL_GAME_WINNINGS / 2)
            purple_team.record[1] += 1
            purple_team.money += int(NORMAL_GAME_WINNINGS / 2)
            return 'tie'
        else:
            purple_team.record[0] += 1
            purple_team.money += NORMAL_GAME_WINNINGS
            blue_team.record[2] += 1
            return purple_team.name

def newGame():
    pass

def saveGame(game, filename):
    with open(filename, 'wb') as f:
        pickle.dump(game, f)

def loadGame(file):
    pass

game = Game()
while True:
    game.nextDay()
                

        



        

    
