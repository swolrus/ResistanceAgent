class Generator:
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.index = 0
        self.rows = []

    def add(self, x, y):
        row = (x, y)
        self.rows.append(row)

    def clear(self):
        self.data = []

    def __next__(self):
        data_ = []
        while self.index < self.batch_size:
            data_.append(self.rows[self.index % len(self.rows)])
            self.index += 1
        self.index = self.index % self.batch_size
        return data_
