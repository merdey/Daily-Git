import pickle, math, sys, random

LEAGUE_SIZE = 4
TEAM_SIZE = 6
GAME_DAY_ACTIONS = ['rest', 'play', 'train']
OFF_DAY_ACTIONS = ['rest', 'train', 'stream']
MIN_SALARY = 5
NORMAL_GAME_WINNINGS = 100

class Player:
    def __init__(self, name, skill, potential, weekly_salary):
        self.name = name
        self.skill = skill
        self.potential = potential
        self.stamina = 100
        self.action = 'rest'
        self.weekly_salary = weekly_salary
        self.money = 0

    def takeAction(self):
        if self.action == 'rest':
            self.stamina = min(self.stamina + 25, 100)
            self.detrain(2)
        elif self.action == 'train':
            self.stamina -= 10
            self.train()
        elif self.action == 'stream':
            self.stamina -= 5
            self.money = 50
            self.detrain(1)
        elif self.action == 'play':
            self.stamina -= 20

    def train(self):
        training_effect = self.potential * .03
        self.skill = min(self.skill + training_effect, 100)

    def detrain(self, severity):
        regression_effect = ((100 - self.potential) * .01) * severity
        self.skill = max(self.skill - regression_effect, 1)

    def __str__(self):
        return self.name + ' skill:' + str(self.skill) + ' stamina:' + str(self.stamina) + ' weekly salary:' + str(self.weekly_salary) + ' last action:' + self.action

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.record = [0, 0, 0]
        self.money = 500

    def collectStreamIncome(self):
        for player in self.players:
            self.money += player.money
            player.money = 0

    def paySalaries(self):
        for player in self.players:
            self.money -= player.weekly_salary

    def setPlayerActions(self, type_of_player, actions_list):
        if type_of_player == 'human':
            print(self)
            for player in self.players:
                print('what would you like ' + player.name + ' to do today?')
                action = input()
                while action not in actions_list:
                    print('invalid action')
                    action = input()
                player.action = action
        else:
            for player in self.players:
                action = random.choice(actions_list)
                player.action = action

    def takePlayerActions(self):
        for player in self.players:
            player.takeAction()

    def isGameReady(self):
        playersReady = 0
        for player in self.players:
            if player.action == 'play':
                playersReady += 1

        return (playersReady == 5)

    def __str__(self):
        s = self.name + '\n'
        for player in self.players:
            s += str(player) + '\n'
        s += 'Record ' + str(self.record) + '\n'
        s += 'Money ' + str(self.money) + '\n'
        return s

class League:
    def __init__(self, teams):
        self.teams = teams

    def generateWeeklyMatchups(self):
        matchups = []
        random.shuffle(self.teams)
        for i in range(0, LEAGUE_SIZE, 2):
            matchups.append( [self.teams[i], self.teams[i + 1]] )
        return matchups

    def generatePlayoffBracket(self):
        seeds = []
        for team in self.teams:
            seeds.append(team)
        return seeds

    def __str__(self):
        s = ''
        for team in self.teams:
            s += str(team) + '\n\n'
        return s

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
        
def generateRandomPlayer():
    names = ['x', 'hotshot', 'GG', 'bigfat', 'Dinh', 'stomp', 'aphro', 'qt', 'pie', 'jiji', 'ima', 'dyrus', 'noscopez', '420']
    name = random.choice(names) + random.choice(names)

    skill = random.randrange(1, 80)
    potential = random.randrange(1, 100)
    weekly_salary = max(int(random.randrange(15, 30) * (skill / 100)), MIN_SALARY) #weekly salary starts at 15-30% of skill, must be at least MIN_SALARY
    
    return Player(name, skill, potential, weekly_salary)

def generateRandomTeam():
    names = ['TSM', 'CLG', 'C9', 'M5', 'CRS', 'Fnatic', 'Dignitas']
    name = random.choice(names)
    
    players = []
    for i in range(TEAM_SIZE):
        players.append(generateRandomPlayer())
    
    return Team(name, players)

def newLeague():
    player_team = generateRandomTeam()
    league_teams = [player_team]
    for i in range(LEAGUE_SIZE - 1):
        league_teams.append(generateRandomTeam())

    league = League(league_teams)
    return league

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
                

        



        

    
