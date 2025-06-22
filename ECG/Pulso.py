import pandas as pd
import matplotlib.pyplot as plt

class Pulso:
    def __init__(self, signal, sample_index, tipo='desconocido', tiempo=None, ventana=150):
        self.tipo = tipo
        self.tiempo = tiempo
        self.sample_index = sample_index
        self.signal = signal
        self.ventana = ventana

        self.segmento_original = self.extraer_ventana()
        self.segmento_normalizado = []
        self.segmento_suavizado = []

    def extraer_ventana(self):
        inicio = max(0, self.sample_index - self.ventana)
        fin = self.sample_index + self.ventana
        return self.signal[inicio:fin]

    def obtener_color(self):
        if self.tipo == 'N' or self.tipo.lower() == 'normal':
            return 'blue'
        else:
            return 'red'

    def normalizar(self):
        if not self.segmento_original:
            print("Segmento vacío. No se puede normalizar.")
            return
        base = sum(self.segmento_original) / len(self.segmento_original)
        self.segmento_normalizado = [x - base for x in self.segmento_original]

    def suavizar(self, ancho_ventana=5):
        if not self.segmento_normalizado:
            print("Segmento no normalizado. No se puede suavizar.")
            return
        serie = pd.Series(self.segmento_normalizado)
        self.segmento_suavizado = serie.rolling(window=ancho_ventana, center=True).mean().bfill().ffill()

    def graficar_original(self):
        color = self.obtener_color()
        plt.plot(self.segmento_original, color=color)
        plt.title(f"Pulso original - Índice {self.sample_index}")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud (mV)")
        plt.grid(True)
        plt.show()

    def graficar_normalizado(self):
        color = self.obtener_color()
        plt.plot(self.segmento_normalizado, color=color)
        plt.title(f"Pulso normalizado - Tipo: {self.tipo}")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud (normalizada)")
        plt.grid(True)
        plt.show()

    def graficar_suavizado(self):
        color = self.obtener_color()
        plt.plot(self.segmento_suavizado, color=color)
        plt.title(f"Pulso suavizado - Tipo: {self.tipo}")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud (suavizada)")
        plt.grid(True)
        plt.show()


    def __repr__(self):
        return f"Pulso en {self.sample_index} - Tipo: {self.tipo} - Tiempo: {self.tiempo}"
