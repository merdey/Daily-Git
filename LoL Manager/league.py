import team

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

LEAGUE_SIZE = 4
STARTING_TEAM_SIZE = 6
def newLeague():
    player_team = team.generateRandomTeam(STARTING_TEAM_SIZE)
    league_teams = [player_team]
    for i in range(LEAGUE_SIZE - 1):
        league_teams.append(team.generateRandomTeam(STARTING_TEAM_SIZE))

    league = League(league_teams)
    return league
