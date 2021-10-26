from game import Game, Round


class Gym(Game):
    def play(self):
        leader_id = 0
        for i in range(5):
            self.rounds.append(Round(leader_id, self.agents, self.spies, i))
            if not self.rounds[i].play():
                self.missions_lost += 1
            for a in self.agents:
                a.round_outcome(i + 1, self.missions_lost)
            leader_id = (
                leader_id + len(self.rounds[i].missions)) % len(self.agents)
        for a in self.agents:
            a.game_outcome(self.missions_lost > 2, self.spies)
