from ECG.Estudio import EstudioECG

nombre_estudio = "100"
estudio = EstudioECG(nombre_estudio)

print(estudio)

latidos_MaxRelativos = estudio.detectarLatidosMaxRelativos()
latidos_SleepECG = estudio.detectarLatidosSleepECG()
print(latidos_MaxRelativos)
print(latidos_SleepECG)

# EJ 2.b) iv.
estudio.compararLatidosPorMetodo()

# EJ 2. c)
estudio.graficarLatidosCorto(segundo_inicio=30, segundos=5)
print("Información adicional proporcionada por metodos de SleepECG:")
estudio.compararConAnotaciones()

# EJ 2. d)
estudio.detectarPulsosAnormales()
estudio.graficarPulsosAnormales(inicio_segundos=5.9*60, duracion_segundos=2)
estudio.graficarPulsosAnormales(inicio_segundos=0, duracion_segundos=30*60)

# EJ 3
estudio.analizarAnnotation(7)
estudio.analizarAnnotation(8)
