class Generator:
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.index = 0
        self.x_hold = None
        self.rows = []

    def add(self, x, y):
        row = (x, y)
        self.rows.append(row)

    def add_x(self, x):
        if not self.x_hold:
            self.x_hold = x
        else:
            raise BufferError('Already have stored an x value! (x={})'.format(str(self.x_hold)))

    def add_y(self, y):
        if self.x_hold:
            row = (self.x_hold, y)
            self.rows.append(row)
        else:
            raise BufferError('X Value required! (Generator.add_x({}))'.format(str(self.x_hold)))

    def get_data_length(self):
        return len(self.data)

    def clear(self):
        self.data = []

    def __next__(self):
        data_ = []
        while self.index < self.batch_size:
            data_.append(self.rows[self.index % len(self.rows)])
            self.index += 1
        self.index = self.index % self.batch_size
        return data_
