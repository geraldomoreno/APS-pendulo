import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    r"C:\Users\Casa\Downloads\trabalho_pendulo\posicoes.csv",
    delimiter=";"
)

# Centraliza em torno da média
x = df["x(px)"] - df["x(px)"].mean()
y = df["y(px)"] - df["y(px)"].mean()
t = df["t(s)"]

print(f"Amplitude em x: {x.std():.1f} px")
print(f"Amplitude em y: {y.std():.1f} px")
print(f"Razão Δy/Δx: {y.std()/x.std():.3f}  (deve ser << 1)")

plt.figure(figsize=(12, 5))
plt.plot(t, x, label="x (horizontal)", linewidth=1)
plt.plot(t, y, label="y (vertical)", alpha=0.7, linewidth=1)
plt.xlabel("Tempo (s)")
plt.ylabel("Posição (px)")
plt.legend()
plt.title("Comparação das variações em x e y")
plt.tight_layout()
plt.savefig(r"C:\Users\Casa\Downloads\trabalho_pendulo\variacao_xy.png", dpi=150)
plt.show()