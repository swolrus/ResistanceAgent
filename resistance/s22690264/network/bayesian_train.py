import operator
from random import random, randrange
from agent import Agent
from s22690264.belief_states import Belief


class BayesianTrainAgent(Agent):
    '''
    The basic random agent extended to include some minimal logic rules
    These rules center around a sus list containing suspicion values for each player
    '''

    def __init__(self, name='Learn'):
        '''
        Initialises the agent.
        '''
        self.name = name
        self.confusion = 0.5

    def reset(self):
        # player stats, each index is the toal suspicion points awarded
        self.rnd_stats = [1] * self.n_players

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

        self.random_agent = RandomAgent()

        self.beliefs = Belief()
        self.beliefs.calc_states(self.n_players, len(self.spy_list))
        self.beliefs.bayesian([self.player_number], 0)

        self.stats = [0] * self.n_players
        self.rnd_stats = [1] * self.n_players

        self.n_round = 1
        self.n_try = 1

    def is_spy(self):
        '''
        returns True if the agent is a spy
        '''
        return self.player_number in self.spy_list

    def propose_mission(self, team_size, betrayals_required=1):
        '''
        if agent is spy use GoodSpy subclass to build team, otherwise build model team off accumulative stats
        use bayesian function to test if team exists and is in the top half of probable distributions
        '''
        return self.random_agent.propose(team_size, self.player_number, self.n_players)

    def vote(self, mission, proposer):
        '''
        always try approve missions where we were the proposer
        if spy use GoodSpy to vote (a variation of random)
        if not spy use similar bayesian strategy as in propose to deny high suspect missions
        '''
        return self.random_agent.vote()

    def vote_outcome(self, mission, proposer, votes):
        '''
        give agents rewards for failed votes if they are:
          - on the mission
          - leader of the mission
        '''
        if not self.is_spy():
            vote_ratio = float(len(votes) / self.n_players)
            if (vote_ratio <= 0.5):
                for agent in range(self.n_players):
                    reward = 0
                    if agent in mission:
                        reward = 2
                        if agent is proposer:
                            reward = 5
                    self.rnd_stats[agent] += reward

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise.
        By default, spies will betray 30% of the time.
        '''
        if self.is_spy():
            return self.random_agent.betray()

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        give agents rewards for failed rounds if they are:
          - on the mission
          - leader of the mission
        '''
        if not self.is_spy():
            if not mission_success:
                for agent in range(self.n_players):
                    reward = 0
                    if agent in mission:
                        reward = 5
                        if agent is proposer:
                            reward = 10
                    self.rnd_stats[agent] += reward
                self.beliefs.bayesian(mission, 1, betrayals)

            self.beliefs.bayesian_suspicion(self.rnd_stats)
            for i in range(self.n_players):
                self.stats[i] += self.rnd_stats[i]

            self.rnd_stats = [1] * self.n_players
            self.n_try = 1
            self.n_round += 1

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
        self.spies_win = spies_win
        pass


class RandomAgent:
    def propose(self, team_size, player_number, n_players):
        team = []
        team.append(player_number)

        while len(team) < team_size:
            agent = randrange(n_players)
            if agent not in team:
                team.append(agent)
        return team

    def vote(self):
        return random() < 0.5

    def betray(self):
        return random() < 0.3
