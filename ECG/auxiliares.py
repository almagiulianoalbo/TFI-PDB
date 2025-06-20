from datetime import datetime

def restar_tiempos(t_final: str, t_inicial: str):
    """
    Resta dos tiempos y devuelve el resultado en segundos.
    """
    from datetime import datetime

    formato = "%M:%S.%f"

    tiempo_final = datetime.strptime(t_final, formato)
    tiempo_inicial = datetime.strptime(t_inicial, formato)

    diferencia = tiempo_final - tiempo_inicial

    return diferencia.total_seconds()


def convertir_a_segundos(tiempo_str):
    dt = datetime.strptime(tiempo_str, "%M:%S.%f")
    return dt.minute * 60 + dt.second + dt.microsecond / 1e6