import operator
from agent import Agent
from s22690264.belief_states import Belief
from s22690264.bots.goodspy import GoodSpy


class BayesianAgent(Agent):
    '''
    The basic random agent extended to include some minimal logic rules
    These rules center around a sus list containing suspicion values for each player
    '''

    def __init__(self, name='Learn'):
        '''
        Initialises the agent.
        '''
        self.name = name
        self.deny_range = 1

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

        if self.is_spy():
            self.spy_agent = GoodSpy(0.1)
            self.spy_agent.new_game(self.spy_list, self.player_number, self.n_players)
        else:
            self.beliefs = Belief()
            self.beliefs.calc_states(self.n_players, len(spy_list))

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
        team = []

        if not self.is_spy():
            for _ in range(2):
                team.append(self.player_number)
                if len(team) == 0:
                    sus_copy = [[i, self.stats[i]] for i in range(len(self.stats))]
                    sus_copy = sorted(sus_copy, key=operator.itemgetter(1))
                    match = self.n_players - Agent.spy_count[self.n_players]

                    spies = []
                    for i in reversed(range(team_size - 1)):
                        if i not in team and len(spies) < Agent.spy_count[self.n_players]:
                            spies.append(i)
                            team.append(sus_copy[i][0])
                    ordered = self.top_states()
                    for i in range(self.deny_range):
                        count = 0
                        for j in range(self.n_players):
                            if ordered[i][0][j] not in team:
                                count += 1
                    if match == count:
                        team = []

        else:
            team = self.spy_agent.propose(team_size)

        return team

    def vote(self, mission, proposer):
        '''
        always try approve missions where we were the proposer
        if spy use GoodSpy to vote (a variation of random)
        if not spy use similar bayesian strategy as in propose to deny high suspect missions
        '''
        if self.player_number is proposer:
            return True
        if self.is_spy():
            return self.spy_agent.vote(mission, proposer)
        elif sum(self.stats) > 0:
            # if is resistance, sort the suspicion
            sus_copy = [[i, self.stats[i]] for i in range(0, len(self.stats))]
            sus_copy = sorted(sus_copy, key=operator.itemgetter(1), reverse=True)
            for i in range(self.deny_range):
                if sus_copy[i] == self.player_number:
                    i += 1
                # test the top most sus agents against the mission agents
                if sus_copy[i] in mission:
                    # will deny missions with one of the top up to deny_range most sus players
                    return False
        # every other mission is approved
        return True

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
            return self.spy_agent.betray(mission, proposer)

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
        pass

    def top_states(self):
        ordered = [[self.beliefs.p_states[i], self.beliefs.beliefs[i]] for i in range(len(self.beliefs.p_states))]
        top = sorted(ordered, key=operator.itemgetter(1), reverse=True)
        return top

    def get_correct_rank(self, true_state):
        ordered = sorted(self.beliefs.beliefs.items(), key=lambda i: i[1], reverse=True)
        rank = 0
        for i in ordered:
            if self.beliefs.p_states[i[0]] == true_state:
                return rank
            rank += 1
