import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

df = pd.read_csv(
    r"C:\Users\Casa\Downloads\trabalho_pendulo\posicoes.csv",
    delimiter=";"
)

t = df["t(s)"].values
x = df["x(px)"].values - df["x(px)"].mean()

#funcao da posicao do oscilador harmonico amortecido
def oha(t, A, b, omega, phi):
    return A * np.exp(-b * t) * np.cos(omega * t + phi)

T_est = 1.55
omega_est = 2 * np.pi / T_est
p0 = [max(abs(x)), 0.01, omega_est, 0]

popt, pcov = curve_fit(oha, t, x, p0=p0, maxfev=10000)
perr = np.sqrt(np.diag(pcov))

A, b, omega, phi = popt
Q = omega / (2 * b)
T = 2 * np.pi / omega

print(f"A = {A:.2f} ± {perr[0]:.2f} px")
print(f"b = {b:.5f} ± {perr[1]:.5f} s⁻¹")
print(f"ω = {omega:.5f} ± {perr[2]:.5f} rad/s")
print(f"φ = {phi:.4f} ± {perr[3]:.4f} rad")
print(f"\nT = {T:.4f} s")
print(f"Q = {Q:.2f}")

# Comparação com valor teórico
L = 0.600  # metros
g = 9.81
T_teorico = 2 * np.pi * np.sqrt(L / g)
print(f"\nT teórico = {T_teorico:.4f} s")
print(f"Desvio = {abs(T - T_teorico)/T_teorico * 100:.2f}%")

# Gráfico
t_fit = np.linspace(t[0], t[-1], 5000)
plt.figure(figsize=(13, 5))
plt.scatter(t, x, s=1, alpha=0.4, label="Dados", color="steelblue")
plt.plot(t_fit, oha(t_fit, *popt), 'r-', linewidth=1.5,
         label=f"Ajuste OHA\nA={A:.1f} px, b={b:.4f} s⁻¹\nω={omega:.4f} rad/s, φ={phi:.3f} rad\nQ={Q:.1f}")
plt.xlabel("Tempo (s)")
plt.ylabel("Posição x (px)")
plt.title("Ajuste do Oscilador Harmônico Amortecido")
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\Casa\Downloads\trabalho_pendulo\ajuste_oha.png", dpi=150)
plt.show()