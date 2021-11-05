from agent import Agent
from s22690264.network.model import Model
from s22690264.bots.goodspy import GoodSpy
from random import randrange


class LearnAgent(Agent):
    '''
    The basic random agent extended to include some minimal logic rules
    These rules center around a sus list containing suspicion values for each player
    '''

    def __init__(self, name='Learn'):
        '''
        Initialises the agent.
        Nothing to do here.
        '''
        self.name = name
        self.newb = True
        self.trained = False
        self.game_count = 1

    def reset(self):
        pass

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        sus is an array of all players, is used to track suspicion when playing as resistance
        '''

        self.n_players = number_of_players
        self.player_number = player_number
        self.spy_list = spy_list
        self.stats = [0] * self.n_players

        self.n_round = 1
        self.n_try = 1

        if self.newb is True:
            self.network = Model([self.n_players, self.n_players, self.n_players * 2], 'sigmoid')
            self.newb = False
            self.train_batch = 1

        if self.is_spy():
            self.spy_agent = GoodSpy(0.1)
            self.spy_agent.new_game(self.spy_list, self.player_number, self.n_players)

        if self.can_train():
            self.game_count += 1
            self.train_batch += 1
            print('learning time!', flush=True)
            self.train()
            self.network.gen.clear()

    def is_spy(self):
        '''
        returns True iff the agent is a spy
        '''
        return self.player_number in self.spy_list

    def propose_mission(self, team_size, betrayals_required=1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned.
        betrayals_required are the number of betrayals required for the mission to fail.
        always places self on
        '''
        team = []
        team.append(self.player_number)

        if not self.is_spy():
            if self.train_batch > 2:
                spies = self.guess_spies()
                for i in range(team_size):
                    most = max(spies)
                    least_likely = spies.index(most)
                    if least_likely != self.player_number:
                        team.append(least_likely)
                    spies[least_likely] = 0
        else:
            team = self.spy_agent.propose(team_size)

        return team

    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        if self.player_number is proposer:
            return True
        if self.is_spy():
            return self.spy_agent.vote(mission, proposer)
        elif self.train_batch > 2:
            spies = self.guess_spies()
            most_likely = max
            most_likely = spies.index(max(spies))
            for agent in mission:
                if agent == most_likely and agent != self.player_number:
                    return False
        return True

    def guess_spies(self):
        if self.train_batch > 2:
            outputs = self.network.predict(self.stats)
            spies = []
            for i in range(self.n_players):
                spies.append(outputs[i * 2] - outputs[i * 2 + 1])
            return spies
        else:
            return None

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        # nothing to do here
        vote_ratio = float(len(votes) / self.n_players)
        if (vote_ratio <= 0.5):
            for agent in range(self.n_players):
                reward = 0
                if agent in mission:
                    reward = 2
                    if agent is proposer:
                        reward = 5
                self.stats[agent] += reward
        self.n_try += 1

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise.
        By default, spies will betray 30% of the time.
        '''

        if self.is_spy():
            return self.spy_agent.betray(mission, proposer)

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission,
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        if not mission_success:
            for agent in range(self.n_players):
                reward = 0
                if agent in mission:
                    reward = 5
                    if agent is proposer:
                        reward = 10
                self.stats[agent] += reward
        self.n_try = 1
        self.n_round += 1

        # print(str(self.totals) + '//' + str(self.stats))
        pass

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        # nothing to do here

        pass

    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        goal = []
        if not self.is_spy():
            for i in range(self.n_players):
                if i in spies:
                    goal.extend([1, 0])
                else:
                    goal.extend([0, 1])
            self.game_count += 1

            self.network.gen.add(self.stats, goal)

    def can_train(self):
        if self.network.gen.get_data_length() > 250 and self.game_count % 100 == 0:
            return True
        else:
            return False

    def train(self):
        self.network.generator_train(10, 20, 1, debug=True)
        self.network.gen.clear()
