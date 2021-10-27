from collections import namedtuple
from itertools import permutations
from agent import Agent


# A state tuple to be attached to each agent tree holding:
# rnd is the round number
# result is the result key [0: denied, 1: failed, 2: success]
# votes_for is the how many times the agent voted for in this state
# includes is how many times agent was included
# was_leader is how many times agent was leader
# totalis the total times state was visited
MISSION_RESULT = ["Denied", "Success", "Fail"]
State = namedtuple("State", "rnd result upvotes includes leaderships total")


class LearnAgent(Agent):

    def __init__(self, name="Learn"):
        self.states = []
        self.name = name
        self.s
        self.first_run = True
        self.discount = 0.9
        self.epsilon = 0.05
        self.max_epsilon = 0.9

    def get_reward(self, game):
        pass


class Player():
    def __init__(self, mission, previous):
        self.previous = previous
        self.action_perm = permutations(range(mission.team_size), mission.number_of_spies)
        self.probabilities = [0] * len(self.action_perm)
        previous.children.append(self)
        self.children = []

    def update(self, mission, agent_id):
        self.state = State(mission.rnd,
                           mission.get_result_key(),
                           int(self.previous.upvotes + voted_for),
                           int(self.previous.includes + included),
                           int(self.previous.leaderships + is_leader),
                           int(self.previous.total + 1))

    def get_result_key(self, mission):
        if not mission.is_approved():
            # "Denied"
            return 0
        if mission.is_successful():
            # "Success"
            return 1
        else:
            # "Failed"
            return 2
