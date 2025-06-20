class Annotations:
    def __init__(self, time, n, type, sub, chan, num):
        self.time = time
        self.numero_samples = n
        self.type = type
        self.subtype = sub
        self.channel = chan
        self.num_repetido = num

    def __repr__(self):
        return f"Tiempo: {self.time} - Cantidad Samples: {self.numero_samples} - Tipo: {self.type} - Subtipo: {self.subtype}"
