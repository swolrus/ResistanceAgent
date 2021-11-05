from s22690264.statistics import Battle
from s22690264.bayesian_accuracy_test import Test
from s22690264.network.model import Model


def main():
    selection = None
    bayesian = False
    partitioned = True
    graph = False
    key = None
    persist = True
    agent_layout = [0, 0, 0, 0]
    while True:
        print('TEST OPTIONS:')
        print('1. Bayesian Graph')
        print('2. Tournament of agents of your choice, batches accumulate')
        print('  3. Above but graphed')
        print('4. Tournament of agents of your choice, batches are partitioned')
        print('  5. Above but graphed')
        try:
            selection = int(input('Please input the integer corresponding: '))
        except ValueError:
            print('Please enter a number.')
        if selection in range(1, 6):
            if selection == 1:
                bayesian = True
            if selection == 3 or 5:
                graph = True
            if selection == 2 or 4:
                partitioned = False
            break
    if selection != 1:
        while True:
            persist = input('Do agents persist between batches? (1=yes, 0=no): ')
            if persist == '0':
                persist = False
                break
            elif persist == '1':
                break
            else:
                print('Enter a valid response.')
        while True:
            try:
                graphed = int(input('Track which percentage? (0=spywins, 1=reswins, 2=totalwins): '))
            except ValueError:
                print('Please enter a number.')
            else:
                if graphed in range(3):
                    key = graphed
                    break
                else:
                    print("Value out of range.")
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
            print('Please enter a number.')
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
        tournament = Battle(agent_layout, graph, key)
        tournament.run(n_batches, n_games, partitioned, 10)


if __name__ == '__main__':
    main()
