# 🫀 Análisis y Procesamiento de Señales ECG  
**Trabajo Final Integrador – Procesamiento de Bioseñales**

---

## 📌 Descripción general

Este proyecto implementa un **pipeline completo de análisis de señales de electrocardiograma (ECG)** utilizando registros reales de la **MIT-BIH Arrhythmia Database**.  
El objetivo es **cargar, procesar, analizar y visualizar señales ECG**, detectar latidos cardíacos, calcular la frecuencia cardíaca y estudiar pulsos normales y anormales mediante técnicas de procesamiento digital de señales y bibliotecas especializadas de Python.

Se utiliza la **MIT-BIH Arrhythmia Database**, que contiene:
Esta base es un estándar internacional para la evaluación de algoritmos de detección y clasificación de arritmias

El desarrollo se apoya en un [`Notebook principal`](./TFI.ipynb) para el análisis exploratorio y validación, junto con una **arquitectura modular orientada a objetos**, que permite reutilizar el código para distintos estudios sin modificaciones estructurales.

---

## 🧠 Objetivos del proyecto

- Leer y procesar estudios ECG a partir de archivos `.csv` y `.txt`
- Centralizar la información del estudio en una **clase Estudio**
- Detectar latidos cardíacos mediante distintos enfoques:
  - Usando anotaciones clínicas
  - A partir del procesamiento de la señal
  - Mediante librerías especializadas de Python
- Calcular la **frecuencia cardíaca promedio y por intervalos**
- Identificar y clasificar **pulsos normales y anormales**
- Extraer, normalizar y suavizar pulsos individuales
- Visualizar señales completas y segmentos específicos del ECG
- Comparar detección automática vs anotaciones de referencia

---

## 🛠️ Tecnologías y librerías utilizadas

- Python 3
- `numpy`
- `pandas`
- `matplotlib`
- `os`
- Librería de detección de ECG (según el método elegido):
  - `sleepecg`
  

