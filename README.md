# Laboratorio: Torque y Momento de Inercia

Repositorio con los scripts de procesamiento de datos, cálculos numéricos y generación de gráficos para el informe de laboratorio sobre Torque ($\tau$) y Aceleración Angular ($\alpha$).

---

##  Estructura del Repositorio

* `codigo_torque.py`: Script principal en Python. Procesa las mediciones experimentales, realiza el ajuste de mínimos cuadrados ponderados, calcula la matriz de covarianza, el coeficiente de correlación $r$ e imprime gráficos de ajuste y residuos.
* `img4/`: Carpeta con las gráficas generadas en formato PDF (ajustes lineales y residuos normalizados). De querer correr el código, debe crear esta carpeta de antemano, o en su defecto, borrar esta dirección en plt.savefig .
* `datos_crudos_torque.xlsx`: mediciones hechas en laboratorio.

---
