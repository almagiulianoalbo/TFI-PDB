from ECG.Annotations import Annotations
from ECG.Registro import Registro
from Lectores import ReadCsv, ReadTxt
from ECG.auxiliares import convertir_a_segundos

# Crear Clase
# Metodo para Calcular frecuencia cardiaca que tome parametros y lo devuelva
# Metodo para detectar latidos

class EstudioECG:
    def __init__(self, nombre: str):
        self.muestras = []              # Lista de Registros
        self.annotations = []           # Lista de Anotaciones
        self.estudio = nombre
        self.CargarEstudio()
        self.frecuencia = self.calcularFrecuenciaCardiaca()

    def CargarEstudio(self):
        csv = ReadCsv(self.estudio)
        txt = ReadTxt(f'{self.estudio}annotations')

        for row in csv.itertuples(index=False):  # Iteramos las filas del .csv
            registro = Registro(row[0], row[1], row[2]) # Crea los registros como clases Registro
            self.muestras.append(registro)

        for i, row in txt.iterrows():
            anotaciones = Annotations(row["Time"], row["Sample"], row["Type"], row["Sub"], row["Chan"], row["Num"])
            self.annotations.append(anotaciones)


    def calcularFrecuenciaCardiaca(self, inicio: str=None, final: str=None) -> float:
        """
        Funcion que calcula frecuencia cardiaca utilizando un intervalo.
        Si uno de los parametros es None, se calcula la frecuencia cardiaca promedio del estudio.
        :param inicio: inicio del intervalo
        :param final: fin del intervalo
        :return: frecuencia cardiaca
        """
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


    def __repr__(self):
        return (f"Estudio: {self.estudio}\n"
                f"Frecuencia Calculada: {self.frecuencia} Hz\n"
                f"Primer muestra: {self.muestras[0]}")


