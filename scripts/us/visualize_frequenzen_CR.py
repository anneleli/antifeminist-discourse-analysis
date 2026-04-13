import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Daten 
jahre = [2021, 2022, 2023, 2024, 2025]
gender_ideology = [5, 2, 22, 15, 19]
gender_theory   = [0, 1,  0,  0,  0]

# Visualisierung
fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(jahre, gender_ideology, label="gender ideology",
        color="#2c7bb6", marker="o", linewidth=2, markersize=6)
ax.plot(jahre, gender_theory, label="gender theory",
        color="#d7191c", marker="s", linewidth=2, markersize=6)

ax.set_xlabel("Jahr", fontsize=12)
ax.set_ylabel("Anzahl Erwähnungen", fontsize=12)
ax.set_title(
    "Häufigkeit antifeministischer Kampfbegriffe im U.S. Congress (2015–2025)",
    fontsize=12, pad=12
)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.set_xlim(2020.7, 2025.3)
ax.set_ylim(bottom=0)
ax.legend(fontsize=11)
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("/Users/Computer/Documents/Studium/Master/MA/CR/frequenzanalyse_congress.png", dpi=150)
plt.show()