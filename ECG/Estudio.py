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
        self.muestras: list[Registro] = []              # Lista de Registros
        self.annotations: list[Annotations] = []           # Lista de Anotaciones
        self.estudio = nombre
        self.cargado = False  # False si aun no se cargan los datos
        self.nombre_signals = [None] * 2

        self.CargarEstudio() # Cargo registros y anotaciones

        self.frecuencia = self.calcularFrecuenciaCardiaca() # BPM
        self.frecuenciaMuestreo = 360 # Hz

    def CargarEstudio(self) -> None:
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

    def calcularFrecuenciaCardiaca(self, inicio: str=None, final: str=None) -> float | None:
        """
        Funcion que calcula frecuencia cardiaca utilizando un intervalo.
        Si uno de los parametros es None, se calcula la frecuencia cardiaca promedio del estudio.

        :param inicio: Comienzo del intervalo
        :param final: Fin del intervalo
        :return: frecuencia cardiaca
        """

        if self.cargado is False: return None

        lista_de_tiempos = []  # Lista de numeros

        for anotacion in self.annotations:
            # Caso: promedio
            if inicio is None or final is None:
                lista_de_tiempos.append(convertir_a_segundos(anotacion.time))

            # Caso: intervalo
            else:
                time = convertir_a_segundos(anotacion.time)
                if inicio <= time <= final:
                    lista_de_tiempos.append(time)

        tiempo_total = lista_de_tiempos[-1] - lista_de_tiempos[0]
        latidos = len(self.annotations)
        frecuencia = 60 * (latidos - 1) / tiempo_total

        return round(frecuencia, 2)

    def detectarLatidosMaxRelativos(self) -> None | list:
        """
        Funcion que detecta latidos maximos relativos
        Realiza el analisis considerando secuencias MLII, V5 o V6 (signal/canal 1)
        :return: Lista de latidos o None si los datos no estan cargados
        """

        channel = self.nombre_signals[0]
        if channel not in ["'MLII'", "'V6'",  "'V5'"]:
            print("Canal no valido")
            return None     # Ignoro otros casos

        latidos = []
        ventana = self.estimar_ventana(bpm_max=int(self.frecuencia))
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
        signals = []

        for signal in self.muestras:
            signals.append(signal.signal1)
        signals = np.array(signals)

        latidos = sleepecg.detect_heartbeats(
            ecg = signals,
            backend = 'c',
            fs = self.frecuenciaMuestreo
        )  # Detectar latidos

        return latidos

    def compararLatidosPorMetodo(self):
        if self.cargado is False: return None
        print(f"LATIDOS: Segun...\n"
        f"Annotations -> {len(self.annotations)}\n"
        f"Max relativo -> {len(self.detectarLatidosMaxRelativos())}\n"
        f"SleepECG -> {len(self.detectarLatidosSleepECG())}\n")
        return None

    # METODOS ADICIONALES DE SleepECG:
    # 1)
    def graficarLatidosCorto(self, segundo_inicio=0, segundos=5):
        """
        Grafica una sección corta de la señal ECG (por defecto 5s) con latidos detectados.
        Ideal para inspección visual clara.
        """

        if not self.cargado:
            print("Estudio no cargado.")
            return

        signal = []
        for reg in self.muestras:
            signal.append(reg.signal1)

        signal = np.array(signal)
        total_muestras = len(signal)

        i_ini = int(segundo_inicio * self.frecuenciaMuestreo)
        i_fin = int((segundo_inicio + segundos) * self.frecuenciaMuestreo)

        if i_fin > total_muestras:
            i_fin = total_muestras
        if i_ini >= total_muestras:
            print("Inicio fuera del rango.")
            return

        signal_corta = signal[i_ini:i_fin]

        # Detectar latidos en la señal completa
        latidos = self.detectarLatidosSleepECG()

        # Filtrar latidos dentro del tramo y ajustar posición relativa
        latidos_visibles = [i - i_ini for i in latidos if i_ini <= i < i_fin]

        # Grafico
        sleepecg.plot_ecg(
            ecg = signal_corta,
            fs = self.frecuenciaMuestreo,
            rpeaks = np.array(latidos_visibles),
            title = f"Latidos entre {segundo_inicio}s y {segundo_inicio + segundos}s"
        )
        plt.show()

    # 2)
    def compararConAnotaciones(self):
        """
        Compara los latidos detectados con SleepECG contra las anotaciones reales.
        Muestra verdaderos positivos, falsos positivos y negativos.
        """
        if not self.cargado:
            print("Estudio no cargado.")
            return

        fs = 360
        latidos_detectados = self.detectarLatidosSleepECG()
        latidos_reales = [int(convertir_a_segundos(a.time) * fs) for a in self.annotations]

        true_positives, false_positives, false_negatives = sleepecg.compare_heartbeats(
            detection = np.array(latidos_detectados),
            annotation = np.array(latidos_reales),
            max_distance = int(0.1 * fs)  # 100ms de tolerancia
        )

        print(f"🔎 Comparación de latidos (SleepECG vs Anotaciones)")
        print(f"✔️ Verdaderos positivos: {len(true_positives)}")
        print(f"❌ Falsos positivos: {len(false_positives)}")
        print(f"⚠️ Falsos negativos: {len(false_negatives)}")


    # Pulsos: N / A

    def detectarPulsosAnormales(self, mostrar=True):
        """
        Detecta latidos anormales en las anotaciones y los retorna.
        Opcionalmente imprime información útil.
        """
        if not self.cargado:
            print("Estudio no cargado.")
            return None

        latidos_anormales = []

        for anotacion in self.annotations:
            if anotacion.type != 'N':           # Anormal
                latidos_anormales.append({
                    'tipo': anotacion.type,
                    'muestra': anotacion.numero_samples,
                    'segundo': convertir_a_segundos(anotacion.time)
                })

        if mostrar:
            print(f"Se encontraron {len(latidos_anormales)} pulsos anormales:\n")
            for latido in latidos_anormales:
                muestra = latido['muestra']

                if muestra < 100: muestra = f'{muestra}  '
                else: f'{muestra}'

                print(f" - Tipo: {latido['tipo']}\t| Muestra: {muestra} \t| Tiempo: {latido['segundo']:.2f} s")

        return latidos_anormales

    def graficarPulsosAnormales(self, inicio_segundos, duracion_segundos):
        """
        Grafica los pulsos anormales dentro de un intervalo específico.
        Solo se muestran los latidos con tipo distinto de 'N' (normal).
        """
        if not self.cargado:
            print("Estudio no cargado.")
            return

        signal = []
        for r in self.muestras:
            signal.append(r.signal1)

        # Buscar latidos anormales dentro del intervalo
        latidos_anormales = self.detectarPulsosAnormales(mostrar=False)
        latidos_anormales_sample = []
        for latido in latidos_anormales:
            latidos_anormales_sample.append(latido['muestra'])

        if not latidos_anormales:
            print("No hay latidos anormales en este intervalo.")
        else:
            print(f"Latidos anormales encontrados: {len(latidos_anormales)}")

        # Graficar
        sleepecg.plot_ecg(
            ecg = np.array(signal),
            fs = self.frecuenciaMuestreo,
            
            rpeaks3 = np.array(latidos_anormales_sample),
            title = f"Latidos anormales entre {inicio_segundos}s y {inicio_segundos + duracion_segundos}s"
        )
        plt.show()

    def estimar_ventana(self, bpm_max: int = 180) -> int:
        segundos_entre_latidos = 60 / bpm_max
        muestras_entre_latidos = segundos_entre_latidos * self.frecuenciaMuestreo
        return int(muestras_entre_latidos / 2)

    def __repr__(self):
        if self.cargado is False:
            return "Estudio no cargado"

        return (f"Estudio: {self.estudio}\n"
                f"Frecuencia Calculada: {self.frecuencia} BPM\n"
                f"Primer muestra: {self.muestras[0]}\n")
