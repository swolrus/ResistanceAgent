from random import randrange, seed
from datetime import datetime


class Generator:
    def __init__(self):
        self.n_folds = 0
        self.fold_size = 0
        self.index = 0
        self.data = []
        self.split = list()

    def __str__(self):
        s = 'Generator holding: ' + str(self.n_folds) + ' folds of size ' + str(self.fold_size) + ', currently at index ' + str(
            self.index) + ' last used batch size was: ' + str(self.batch_size)
        return s

    def add(self, x, y):
        row = [x, y]
        self.data.append(row)

    def split_data(self, batch_size):
        seed(datetime.now())
        self.batch_size = batch_size
        self.index = 0
        self.split = list()
        data_ = self.data.copy()
        self.n_folds = int(len(self.data) / self.batch_size)
        for i in range(self.n_folds):
            fold = list()
            while len(fold) < self.batch_size and len(data_) > 0:
                j = randrange(len(data_))
                fold.append(data_.pop(j))
            self.split.append(fold)

    def get_data_length(self):
        return len(self.data)

    def clear(self):
        self.split = list()
        self.index = 0
        self.n_folds = 0

    def __next__(self):
        self.index += 1
        return self.split[self.index % self.n_folds]
