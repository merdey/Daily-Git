import random, player

class Team:
    def __init__(self, name, players, money):
        self.name = name #team name
        self.players = players #list of players
        self.record = [0, 0, 0] #Wins-Ties-Losses
        self.money = money

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

STARTING_TEAM_MONEY = 500
NAMES = ['TSM', 'CLG', 'C9', 'M5', 'CRS', 'Fnatic', 'Dignitas']
def generateRandomTeam(team_size):
    name = random.choice(NAMES)
    
    players = []
    for i in range(team_size):
        players.append(player.generateRandomPlayer())
        
    money = STARTING_TEAM_MONEY
    
    return Team(name, players, money)
