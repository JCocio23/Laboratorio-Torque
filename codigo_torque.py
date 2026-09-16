import numpy as np
import matplotlib.pyplot as plt

def graficar_ajuste_y_residuos(alpha, dalpha, tau, dtau, radio):
    # Ajuste lineal con residuos y obtención de la matriz de covarianza
    (m, b), cov = np.polyfit(alpha, tau, 1, w=1/dtau, cov=True)
    
    # Incertidumbres a partir de la diagonal de la matriz de covarianza
    dm = np.sqrt(cov[0, 0])
    db = np.sqrt(cov[1, 1])
    
    # Coeficiente de correlación de Pearson (r)
    r = np.corrcoef(alpha, tau)[0, 1]
    
    # Muestra los resultados en la terminal     
    print("Matriz de Covarianza:")
    print(cov)
    print(f"Pendiente (m):     {m:.6e} +/- {dm:.6e}")
    print(f"Intercepto (b):    {b:.6e} +/- {db:.6e}")
    print(f"Coeficiente r:     {r:.6f}")
    print(f"Coeficiente R^2:   {r**2:.6f}")
    print("=" * 45 + "\n")
    
    # Ajuste y residuos normalizados
    tau_ajuste = m * alpha + b
    residuos = tau - tau_ajuste
    residuos_norm = residuos / dtau      
    # Gráfico de ajuste
    plt.figure(figsize=(6, 4))
    plt.errorbar(alpha, tau, xerr=dalpha, yerr=dtau, fmt='o', capsize=3, label='Datos experimentales')
    
    # Recta del ajuste para el dibujo
    alpha_linea = np.linspace(min(alpha), max(alpha), 100)
    tau_linea = m * alpha_linea + b
    plt.plot(alpha_linea, tau_linea, '-', color='red', label=f'Ajuste: y = {m:.4e}x + {b:.4e}')
    
    plt.xlabel(r'Aceleración angular $\alpha$ [rad/s$^2$]')
    plt.ylabel(r'Torque $\tau$ [N·m]')
    plt.title(f'Torque vs Aceleración angular ({radio})')
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig(f"img4/ajuste3_{radio}.pdf")
    plt.show()

    # Gráfico de residuos
    plt.figure(figsize=(6, 4))
    
    # Residuos normalizados (residuo / error de tau)
    plt.errorbar(alpha, residuos_norm, xerr=dalpha, fmt='o', color='tab:green', capsize=3)
    
    # Línea horizontal en cero
    plt.axhline(0, color='black', linestyle='--', linewidth=1.5)
    plt.axhline(1, color='gray', linestyle=':', linewidth=1)
    plt.axhline(-1, color='gray', linestyle=':', linewidth=1)
    plt.axhline(2, color='gray', linestyle=':', linewidth=0.7)
    plt.axhline(-2, color='gray', linestyle=':', linewidth=0.7)
    plt.xlabel(r'Aceleración angular $\alpha$  [rad/s$^2$]')
    plt.ylabel(r'Residuos normalizados $(\tau_{dato}-\tau_{ajuste})/\delta\tau$')
    plt.title(f'Residuos normalizados del ajuste ({radio})')
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig(f"img4/residuos3_{radio}.pdf")
    plt.show()

    return m, b, residuos_norm


def histograma_residuos_normalizados(residuos_norm, nombre):

    from scipy.stats import norm

    residuos_norm = np.asarray(residuos_norm)
    n = len(residuos_norm)

    plt.figure(figsize=(6, 4))

    # Curva teórica N(0,1)
    x_max = max(4, np.max(np.abs(residuos_norm)) + 1)
    x = np.linspace(-x_max, x_max, 300)
    plt.plot(x, norm.pdf(x, 0, 1), 'r-', linewidth=2, label=r'$N(0,1)$ teórica')
    plt.fill_between(x, norm.pdf(x, 0, 1), color='red', alpha=0.08)

    # Cada residuo como un punto individual sobre el eje (rug plot)
    y_puntos = np.zeros(n)
    plt.scatter(
        residuos_norm, y_puntos, color='tab:green', s=70,
        zorder=5, edgecolor='black', label=f'Residuos normalizados (N={n})'
    )
    # Líneas verticales tipo "rug" para ubicar mejor cada punto
    for r in residuos_norm:
        plt.axvline(r, color='tab:green', alpha=0.3, linewidth=1, ymax=0.08)

    # Bandas de referencia en +/-1, +/-2, +/-3 sigma
    for s, alpha_line in zip([1, 2, 3], [0.5, 0.3, 0.15]):
        plt.axvline(s, color='gray', linestyle=':', linewidth=1, alpha=alpha_line)
        plt.axvline(-s, color='gray', linestyle=':', linewidth=1, alpha=alpha_line)

    plt.axhline(0, color='black', linewidth=0.8)
    plt.xlabel(r'Residuo normalizado $(\tau_{dato}-\tau_{ajuste})/\delta\tau$')
    plt.ylabel('Densidad de probabilidad')
    plt.title(f'Residuos normalizados vs. $N(0,1)$ ({nombre})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"img4/residuos_puntos_3_{nombre}.pdf")
    plt.show()

# Datos para r = 2.505 cm
a1 = np.array([0.28222, 0.9182, 1.8749, 3.5193, 5.1353])
da1 = np.array([0.00072, 0.0047, 0.0048, 0.0049, 0.0074])
t1 = np.array([0.0026471, 0.0076335, 0.015048, 0.027142, 0.039330])
dt1 = np.array([0.0000029, 0.0000077, 0.000015, 0.000034, 0.000048])

m1, b1, res_norm1 = graficar_ajuste_y_residuos(a1, da1, t1, dt1, "r = 2.505 cm")
histograma_residuos_normalizados(res_norm1, "r = 2.505 cm")

# Datos para r = 2.005 cm
a2 = np.array([0.1959, 1.0071, 1.5657, 2.9009, 3.737])
da2 = np.array([0.0016, 0.0055, 0.0079, 0.0072, 0.016])
t2 = np.array([0.0020682, 0.008034, 0.011963, 0.021768, 0.027676])
dt2 = np.array([0.0000028, 0.000010, 0.000015, 0.000028, 0.000035])

m2, b2, res_norm2 = graficar_ajuste_y_residuos(a2, da2, t2, dt2, "r = 2.005 cm")
histograma_residuos_normalizados(res_norm2, "r = 2.005 cm")

# Datos para r = 1.570 cm
a3 = np.array([0.1282, 0.75059, 1.1542, 2.1928, 2.7931])
da3 = np.array([0.0016, 0.00084, 0.0071, 0.0048, 0.0079])
t3 = np.array([0.0016198, 0.006294, 0.009368, 0.017094, 0.021748])
dt3 = np.array([0.0000027, 0.000010, 0.000015, 0.000027, 0.000035])

m3, b3, res_norm3 = graficar_ajuste_y_residuos(a3, da3, t3, dt3, "r = 1.570 cm")
histograma_residuos_normalizados(res_norm3, "r = 1.570 cm")
