import itertools
from agent import Agent


class BeliefStates():
    def __init__(self, n_players, game):
        self.n_players = n_players
        self.calc_states(n_players, Agent.spy_count[n_players])
        self.beliefs = []
        for agent in range(self.n_players):
            b = Belief(self.p_states)
            if agent in game.spies:
                look = 1
            else:
                look = 0
            b.bayesian([agent], None, look)
            self.beliefs.append(b)

    def __str__(self):
        s = 'AGENT BELIEF STATES\n'
        for i in range(len(self.beliefs)):
            s += 'AGENT ' + str(i) + '\n' + str(self.beliefs[i]) + '\n'
        return s

    def calc_states(self, n_players, n_spies):
        roles = list(range(self.n_players))
        c_spy = list(itertools.combinations(roles, 2))
        self.n = len(c_spy)
        self.p_states = [tuple(1 if i in c else 0 for i in roles) for c in c_spy]

    def bayesian(self, indexes, zero):
        for b in self.beliefs:
            b.bayesian(indexes, zero)


class Belief():
    def initialise(self, p_states):
        self.p_states = p_states
        self.n = len(self.p_states)
        self.beliefs = {i: 1. / self.n for i in range(self.n)}

    def __str__(self):
        s = str(self.beliefs) + '\n'
        for i in range(len(self.p_states)):
            s += str(self.p_states[i]) + '-> ' + str(self.beliefs[i]) + '\n'
        return s

    def calc_states(self, n_players, n_spies):
        self.n_players = n_players
        roles = list(range(n_players))
        c_spy = list(itertools.combinations(roles, 2))
        self.n = len(c_spy)
        self.p_states = [tuple(1 if i in c else 0 for i in roles) for c in c_spy]
        self.initialise(self.p_states)

    def bayesian(self, indexes, match, n_spies=None):
        touched = False
        H = {}
        for i in range(len(self.p_states)):
            matches = 0
            for j in indexes:
                if self.p_states[i][j] == match:
                    matches += 1
                    if touched is False and self.beliefs[i] > 0:
                        H[i] = self.beliefs[i]
                        touched = True

            if n_spies is not None and len(indexes) == n_spies and i in H:
                del H[i]

            matches = 0
            touched = False
        if len(H) != 0:
            p_H = 1 / sum([H[i] for i in H.keys()])

            for i in range(len(self.beliefs)):
                if i in H.keys():
                    self.beliefs[i] = p_H * H[i]
                else:
                    self.beliefs[i] = 0.

            self.n = len(H)

    def bayesian_suspicion(self, dist):
        H = {}
        d_max = max(dist)
        for i in range(len(self.p_states)):
            if self.beliefs[i] != 0:
                r = 0
                for j in range(self.n_players):
                    if self.p_states[i][j] == 1:
                        r += dist[j]
                    else:
                        r += d_max - dist[j] 

                if r != 0:
                    H[i] = r * self.beliefs[i]
                else:
                    del H[i]

        total = sum(H[i] for i in H.keys())
        for i in range(len(self.p_states)):
            if i in H.keys():
                self.beliefs[i] = H[i] / total
            else:
                self.beliefs[i] = 0.
