from random import randrange, random


class GoodSpy:
    def __init__(self, confusion):
        self.plays = 0
        self.wins = 0
        self.confusion = confusion
        self.failed_missions = 0

    def new_game(self, spy_list, player_number, n_players):
        self.n_players = n_players
        self.player_number = player_number
        self.spy_list = spy_list
        return self

    def propose(self, team_size):
        team = []
        team.append(self.player_number)

        while len(team) < team_size:
            agent = randrange(self.n_players)
            if agent not in team:
                team.append(agent)
        return team

    def vote(self, mission, proposer):
        if proposer == self.player_number:
            return True
        # confusion
        if random() < 1 - self.confusion:
            return False
        # if is a spy
        for player in mission:
            if player in self.spy_list:
                # approve missions with any spy in them
                return True

    def betray(self, mission, proposer):
        if proposer == self.player_number:
            return True
        spy_count = 0
        for agent in mission:
            if agent in self.spy_list:
                spy_count += 1
        return random() < ((1 / spy_count) + self.confusion)
