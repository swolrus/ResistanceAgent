from agent import Agent
import random
import operator
from s22690264.network.model import Model
from s22690264.network.generator import Generator


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
        self.network = Model(1, (4, 8, 2))
        self.gen = Generator(10)

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        sus is an array of all players, is used to track suspicion when playing as resistance
        '''
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spy_list = spy_list

        # players [went on failed miss, proposed failed miss]
        self.stats = {}
        for i in range(self.number_of_players):
            self.stats[i] = [0, 0]
        self.totals = [0, 0]

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
            spies = self.guess_spies()
            for i in range(team_size):
                if i not in spies and i != self.player_number:
                    team.append(i)
        else:
            while len(team) < team_size:
                agent = random.randrange(team_size)
                if agent not in team:
                    team.append(agent)

        return team

    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        if self.is_spy():
            # if is a spy
            for player in mission:
                if player in self.spy_list:
                    # approve missions with any spy in them
                    return True
            # deny if no spies in mission
            return False

        elif self.train_batch > 0:
            spies = self.guess_spies()
            # if is resistance, sort the suspicion
            for i in range(len(spies)):
                # deny if most sus up to number of spies is on mission
                if spies[i] in mission:
                    # will deny missions with one of the top up to deny_range most sus players
                    return False
            # every other mission is approved
            return True
        else:
            # Denies missions if no data yet
            return False

    def guess_spies(self):
        spies = [[0, 0] for i in range(self.number_of_players)]
        for key, value in self.stats.items():
            spies[key][0] = key
            inputs = [0] * 4
            if self.totals[0] != 0:
                inputs[0] = value[0]
                inputs[1] = self.totals[0]
            if self.totals[1] != 0:
                inputs[2] = value[1]
                inputs[3] = self.totals[1]
            print(inputs)
            spies[key][1] = self.network.predict(inputs)
        print(spies)
        return spies

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        # nothing to do here
        vote_ratio = sum(votes) / self.number_of_players
        if (vote_ratio < 1/2):
            self.stats[proposer][1] += 1
            self.totals[1] += 1
        pass

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise.
        By default, spies will betray 30% of the time.
        '''
        spy_count = 0
        for agent in mission:
            if agent in self.spy_list:
                spy_count += 1
        return random.random() < (1 / spy_count)

        return True

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
            for agent in mission:
                self.stats[agent][0] = self.stats[agent][0] + 1
                self.totals[0] = self.totals[0] + 1

        #print(str(self.totals) + '//' + str(self.stats))
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
        # nothing to do here
        # print(str(self.stats) + '// ' + str(self.totals))
        # goal = [0] * self.number_of_players
        # inputs = [0] * (self.number_of_players * 2)
        # for key, value in self.stats.items():
        #     if self.totals[0] != 0:
        #         inputs[key * 2] = value[0] / self.totals[0]
        #     if self.totals[1] != 0:
        #         inputs[key * 2 + 1] = value[1] / self.totals[1]
        #     if key in spies:
        #         goal[key] = 1
        # self.gen.add(inputs, goal)
        for key, value in self.stats.items():
            if key in spies:
                goal = [0, 1]
            else:
                goal = [1, 0]
            inputs = [0] * 4
            if self.totals[0] != 0:
                inputs[0] = value[0]
                inputs[1] = self.totals[0]
            if self.totals[1] != 0:
                inputs[2] = value[1]
                inputs[3] = self.totals[1]
            self.gen.add(inputs, goal)

        if self.can_train():
            self.train()
            self.gen.clear()
            self.train_batch += 1

    def can_train(self):
        if self.gen.get_data_length() > 100 * self.number_of_players:
            return True
        else:
            return False

    def train(self):
        self.network.generator_train(self.gen, 0.2, 20, anneal=True, anneal_rate=0.99, debug=False)
