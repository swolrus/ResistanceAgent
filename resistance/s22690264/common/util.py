import pickle
import os
from random import seed, shuffle
from datetime import datetime
from s22690264.bots.random import RandomAgent
from s22690264.bots.basic import BasicAgent
from s22690264.bots.basic_learn import LearnAgent
from s22690264.bots.bayesian import BayesianAgent


AGENT_CODES = {
    'Random': [0, RandomAgent],
    'Basic': [1, BasicAgent],
    'Bayesian': [2, BayesianAgent],
    'Learn': [3, LearnAgent],
}

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

COLORS = ['#78B5AC', '#D8D898', '#8482CD', '#800040', '#FD6666']

LAYER_ID = {'INPUT': 0, 'HIDDEN': 1, 'OUTPUT': 2}


def get_sub(s):
    sout = []
    for i in range(len(s)):
        sout.append(str(s[i].translate(SUB)))
    return ''.join(sout)


def get_color(agent):
    if isinstance(agent, RandomAgent):
        color = COLORS[0]
    if isinstance(agent, BasicAgent):
        color = COLORS[1]
    if isinstance(agent, BayesianAgent):
        color = COLORS[2]
    if isinstance(agent, LearnAgent):
        color = COLORS[3]
    return color


def save_obj(obj, name, subfolder=''):
    '''
    Save the neural net in a pickle file
    name is the filename
    subfolder is the subfolder to store under
    '''
    dirname = os.path.dirname(__file__)
    folder = os.path.join(dirname, 'obj', subfolder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    with open(folder + '/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name, subfolder=''):
    '''
    Load a previously pickled net, use same name and subfolder values as when saving
    name is the filename
    subfolder is the subfolder to store under
    '''
    dirname = os.path.dirname(__file__)
    folder = os.path.join(dirname, 'obj', subfolder)
    with open(folder + '/' + name + '.pkl', 'rb') as f:
        obj = pickle.load(f)
    return obj


def get_agent_array(agent_counts):
    agents = []
    num = 0
    for name, info in AGENT_CODES.items():
        for j in range(agent_counts[info[0]]):
            num += 1
            agents.append(info[1](name))
    for i in range(len(agents)):
        agents[i].name = '(' + str(i) + ')' + agents[i].name
    return agents


def shuffle_agents(agents):
    seed(datetime.now())
    shuffle(agents)
    return agents.copy()
