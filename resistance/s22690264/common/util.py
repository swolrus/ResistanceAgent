import pickle
import os


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
