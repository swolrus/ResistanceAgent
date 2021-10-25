from agent import Agent
import random
import operator


class LearnAgent(Agent):
    '''
    The basic random agent extended to include some minimal logic rules
    These rules center around a sus list containing suspicion values for each player
    '''

    def __init__(self, name='Based'):
        '''
        Initialises the agent.
        Nothing to do here.
        '''
        self.name = name

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

        self.sus = [0] * self.number_of_players
        self.sus[self.player_number] = -1

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
        team.append(self)

        if not self.is_spy():
            sus_copy = [[i, self.sus[i]] for i in range(len(self.sus))]
            sus_copy = sorted(sus_copy, key=operator.itemgetter(1))
            for i in range(team_size - 1):
                if i < len(sus_copy) and sus_copy[i - 1][0] not in team:
                    team.append(sus_copy[i - 1][0])

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
        elif sum(self.sus) > 0:
            # if is resistance, sort the suspicion
            sus_copy = [[i, self.sus[i]] for i in range(0, len(self.sus))]
            sus_copy = sorted(sus_copy, key=operator.itemgetter(1), reverse=True)
            for i in range(len(self.spy_list)):
                # deny if most sus up to number of spies is on mission
                if sus_copy[i] in mission:
                    # will deny missions with one of the top up to deny_range most sus players
                    return False
            # every other mission is approved
            return True
        else:
            # Denies missions if no data yet
            return False

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        # nothing to do here
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
            for i in range(len(mission)):
                if i != self.player_number:
                    self.sus[i] = self.sus[i] + 1
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
        pass
