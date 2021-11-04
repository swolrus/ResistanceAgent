from s22690264.statistics import Battle
from s22690264.bayesian_accuracy_test import Test
from s22690264.network.model import Model

def main():
    bayesian = False
    partitioned = True
    graph = False
    graphed = None
    persist = True
    agent_layout = [0, 0, 0, 0]
    while True:
        print('TEST OPTIONS:')
        print('1. Bayesian Graph')
        print('2. Tournament of agents of your choice, batches accumulate')
        print('  3. Above but graphed')
        print('4. Tournament of agents of your choice, batches are partitioned')
        print('  5. Above but graphed')
        selection = int(input('Please input the integer corresponding: '))
        if selection == 1:
            bayesian = True
            break
        if selection == 2 or 3:
            partitioned = False
            while True:
                graphed = int(input('What to graph (0=spywins, 1=reswins, 2=totalwins): '))
                if graphed in range(3):
                    graphed = graphed
                    break
        if selection == 3 or 5:
            graph = True
        if selection in range(1, 6):
            break
    if selection != 1:
        while True:
            persist = input('Do agents persist between batches? (1=yes, 0=no): ')
            if persist == '0':
                persist = False
                break
            elif persist == '1':
                break
    while True:
        print('Enter agent counts.')
        try:
            agent_layout[0] = int(input('Number Random: '))
            agent_layout[1] = int(input('Number Basic: '))
            agent_layout[2] = int(input('Number Bayesian: '))
            agent_layout[3] = int(input('Number Learn: '))
            n_batches = int(input('Enter number of batches: '))
            n_games = int(input('Enter n games per batch: '))
        except ValueError:
            print('Please enter an integer')
        else:
            if 4 < sum(agent_layout) < 11:
                break
            else:
                print('Total agent must be between 5 and 10 agents.')
    if bayesian is True:
        test = Test(agent_layout)
        test.simulate(n_batches, n_games)
        test.plot()
    else:
        tournament = Battle(agent_layout, graph, graphed)
        tournament.run(n_batches, n_games, partitioned, 10)


if __name__ == '__main__':
    main()
