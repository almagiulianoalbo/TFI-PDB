from ECG.Estudio import EstudioECG

nombre_estudio = "100"
estudio = EstudioECG(nombre_estudio)

print(estudio)

# EJ 2.iii
estudio.compararLatidosPorMetodo()

estudio.graficarLatidosCorto(segundo_inicio=30, segundos=5)

print("Información adicional proporcionada por metodos de SleepECG:")
estudio.compararConAnotaciones()

estudio.detectarPulsosAnormales()

estudio.graficarPulsosAnormales(inicio_segundos=5.9*60, duracion_segundos=2)
estudio.graficarPulsosAnormales(inicio_segundos=0, duracion_segundos=30*60)

# EJ 3
estudio.analizarAnnotation(8)
