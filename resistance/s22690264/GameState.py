from collections import deque


class GameState():
    actions = ["VoteDown", "VoteUp"]

    def set_state(self, round):
        self.round = round


class StateTree:
    def __init__(self, data):
        self.previous = None
        self.previous_action = None
        self.actions = []
        self.data = data

    def set_previous(self, previous):
        self.previous = previous
