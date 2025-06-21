from ECG.Annotations import Annotations
from ECG.Registro import Registro
from Lectores import ReadCsv, ReadTxt
from ECG.auxiliares import convertir_a_segundos
import sleepecg
import numpy as np
import matplotlib.pyplot as plt



# Crear Clase
# Metodo para Calcular frecuencia cardiaca que tome parametros y lo devuelva
# Metodo para detectar latidos

class EstudioECG:
    def __init__(self, nombre: str):
        self.muestras = []              # Lista de Registros
        self.annotations = []           # Lista de Anotaciones
        self.estudio = nombre
        self.cargado = False  # False si aun no se cargan los datos
        self.nombre_signals = [None] * 2
        self.CargarEstudio()
        self.frecuencia = self.calcularFrecuenciaCardiaca()


    def CargarEstudio(self):
        csv = ReadCsv(self.estudio)
        txt = ReadTxt(f'{self.estudio}annotations')

        # Si recibo un archivo invalido, termina
        if csv is None or txt is None: return None
        else: self.cargado = True

        self.nombre_signals[0] = csv.columns[1]
        self.nombre_signals[1] = csv.columns[2]

        for row in csv.itertuples(index=False):  # Itera las filas del .csv
            registro = Registro(row[0], row[1], row[2]) # Crea los registros como clases Registro
            self.muestras.append(registro)

        for i, row in txt.iterrows():
            anotaciones = Annotations(row["Time"], row["Sample"], row["Type"], row["Sub"], row["Chan"], row["Num"])
            self.annotations.append(anotaciones)

        return None

    def calcularFrecuenciaCardiaca(self, inicio: str=None, final: str=None) -> float:
        """
        Funcion que calcula frecuencia cardiaca utilizando un intervalo.
        Si uno de los parametros es None, se calcula la frecuencia cardiaca promedio del estudio.
        :param inicio: inicio del intervalo
        :param final: fin del intervalo
        :return: frecuencia cardiaca
        """
        if self.cargado is False: return None

        lista_de_tiempos = []  # Lista de numeros
        if inicio is None or final is None:
            for anotacion in self.annotations:
                lista_de_tiempos.append(convertir_a_segundos(anotacion.time))

        else:
            for anotacion in self.annotations:
                time = convertir_a_segundos(anotacion.time)
                if inicio <= time <= final:
                    lista_de_tiempos.append(time)


        tiempo_total = lista_de_tiempos[-1] - lista_de_tiempos[0]
        latidos = len(self.annotations)
        frecuencia = 60 * (latidos - 1) / tiempo_total
        return round(frecuencia, 2)

    def detectarLatidosMaxRelativos(self):
        """
        Funcion que detecta latidos maximos relativos
        Realiza el analisis considerando secuencias MLII, V5 o V6 (signal/canal 1)
        :return:
        """

        channel = self.nombre_signals[0]
        if channel not in ["'MLII'", "'V6'",  "'V5'"]:
            print("Canal no valido")
            return None     # Ignoro otros casos

        latidos = []
        ventana = estimar_ventana(bpm_max=int(self.frecuencia))
        print(f"Ventana estimada para este estudio: {ventana}\n")
        print(f"CARGANDO...\n")

        # Seteo el intervalo
        for i in range(0, len(self.muestras)):
            entorno = self.muestras[i - ventana : i + ventana + 1]

            # Busco el maximo del intervalo
            maximo = 0
            for registro_entorno in entorno:
                if registro_entorno.signal1 > maximo:
                    maximo = registro_entorno.signal1

            if self.muestras[i].signal1 == maximo:
                latidos.append(i)

        return latidos

    def detectarLatidosSleepECG(self):
        frec_muestreo = 360  # Hz
        signals = []
        for signal in self.muestras:
            signals.append(signal.signal1)
        signals = np.array(signals)

        latidos = sleepecg.detect_heartbeats(ecg=signals, backend='c', fs= frec_muestreo)  # Detectar latidos

        return latidos

    def compararLatidosPorMetodo(self):
        if self.cargado is False: return None
        print(f"LATIDOS: Segun...\n"
        f"Annotations -> {len(self.annotations)}\n"
        f"Max relativo -> {len(self.detectarLatidosMaxRelativos())}\n"
        f"SleepECG -> {len(self.detectarLatidosSleepECG())}\n")
        return None

    def __repr__(self):
        if self.cargado is False: return "Estudio no cargado"

        return (f"Estudio: {self.estudio}\n"
                f"Frecuencia Calculada: {self.frecuencia} BPM\n"
                f"Primer muestra: {self.muestras[0]}\n")



def estimar_ventana(fs: int = 360, bpm_max: int = 180) -> int:
    segundos_entre_latidos = 60 / bpm_max
    muestras_entre_latidos = segundos_entre_latidos * fs
    return int(muestras_entre_latidos / 2)

