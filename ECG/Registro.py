class Registro:
    def __init__(self, sample, signal1, signal2):
        self.sample = sample
        self.signal1 = signal1
        self.signal2 = signal2

    def __repr__(self):
        return f"Sample: {self.sample} - Señal 1: {self.signal1} - Señal 2: {self.signal2}"