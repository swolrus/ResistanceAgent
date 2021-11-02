from random import randrange


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
        row = (x, y)
        self.data.append(row)

    def split_data(self, n_folds):
        self.index = 0
        self.split = list()
        data_ = self.data.copy()
        self.fold_size = int(len(data_) / n_folds)
        for i in range(n_folds):
            fold = list()
            while len(fold) < self.fold_size:
                i = randrange(len(data_))
                fold.append(data_.pop(i))
            self.split.append(fold)
            self.n_folds += 1
        return self.split

    def clear(self):
        self.split = list()
        self.index = 0
        self.n_folds = 0

    def __next__(self):
        return self.split[self.index]
