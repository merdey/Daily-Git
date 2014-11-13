import random

class Player:
    def __init__(self, name, skill, potential, weekly_salary):
        self.name = name #IGN
        self.skill = skill #used for calculating game outcomes
        self.potential = potential #determines by how much skill increases with training/detraining
        self.stamina = 100 #max 100, min 0; decreases as player takes actions other than resting, affects contribution to game outcome
        self.action = 'rest' #tracks action for current time period
        self.weekly_salary = weekly_salary #salary team must pay player every week
        self.money = 0 #personal income gained from streaming, etc; 'taxed' by team every week

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

MIN_SALARY = 5
NAMES = ['x', 'hotshot', 'GG', 'bigfat', 'Dinh', 'stomp', 'aphro', 'qt', 'pie', 'jiji', 'ima', 'dyrus', 'noscopez', '420']
def generateRandomPlayer():
    name = random.choice(NAMES) + random.choice(NAMES)
    skill = random.randrange(1, 80)
    potential = random.randrange(1, 100)
    weekly_salary = max(int(random.randrange(15, 30) * (skill / 100)), MIN_SALARY) #weekly salary starts at 15-30% of skill, must be at least MIN_SALARY
    
    return Player(name, skill, potential, weekly_salary)

if __name__ == '__main__':
    for i in range(10):
        print(str(generateRandomPlayer()))
