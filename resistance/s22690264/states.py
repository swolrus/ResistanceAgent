from s22690264.belief_states import BeliefStates

class States:
    def __init__(self):
        self.number_of_players = 5
        self.events = list()
        self.b_states = BeliefStates(5)

    def __str__(self):
        max_array = str(self.number_of_players * 3 + 2)
        formatting = '{:<4s}| {:<4s}| {:<5s}|{:>' + max_array + 's} | {:<' + max_array + 's}| {:<s}\n'
        s = formatting.format('Rnd', 'Try', 'Lead', 'Team', 'Votes For', 'status')
        s += '=' * (33 + (self.number_of_players * 3 + 1) + 20) + '\n'
        for state in self.events:
            s += formatting.format(str(state.n_round), str(state.n_try), str(state.leader), str(state.team), str(state.votes), state.status)
        return s

    def add(self, n_round, n_try, leader, status, team, votes):
        state = GameState(n_round, n_try, leader, status, team, votes)
        self.events.append(state)

    def set_last_status(self, status):
        self.events[len(self.events) - 1].status = status

    def reveal_spies(self, agents, spy_list):
        self.spy_list = spy_list


class GameState():
    def __init__(self, n_round, n_try, leader, status, team, votes):
        self.n_round = n_round
        self.n_try = n_try
        self.leader = leader
        self.status = status
        self.team = team
        self.votes = votes
