import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

# Failinimed
DATA_FILE = "data.csv"
PLOT_FILE = "plot.png"

# 1. Laeme olemasolevad andmed (kui fail on olemas)
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, parse_dates=["datetime"])
    print("Olemasolevad andmed loetud, ridu:", len(df))
else:
    df = pd.DataFrame(columns=["datetime", "temperature"])
    print("Uus andmefail luuakse")

# Veendume, et datetime veerg on datetime tüüpi
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=False)
df = df.dropna(subset=["datetime"])           # eemaldame vigased read
df = df.sort_values("datetime").drop_duplicates(subset=["datetime"])

# Siin peaks tavaliselt tulema sinu andmete allalaadimise osa
# Näide – asenda see päris andmeallikaga (nt requests + bs4 või API)
# --------------------------------------------------------------------
# Näidisandmed testimiseks (kui päris andmeid veel pole)
if len(df) == 0:
    print("Testandmed, kuna andmeid pole veel")
    test_data = [
        {"datetime": "2025-02-01 00:00", "temperature": -3.2},
        {"datetime": "2025-02-01 01:00", "temperature": -3.8},
        {"datetime": "2025-02-01 02:00", "temperature": -4.1},
    ]
    new_df = pd.DataFrame(test_data)
    new_df["datetime"] = pd.to_datetime(new_df["datetime"])
    df = pd.concat([df, new_df], ignore_index=True)

# Siia tuleb sinu tegelik andmete hankimise kood, nt:
#
# import requests
# from bs4 import BeautifulSoup
#
# url = "https://www.ilmateenistus.ee/ilmaandmed/vaatlused/?id=26229"  # Valga jaam
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# ... leia temperatuur ja aeg ...
# new_row = {"datetime": datetime.now(), "temperature": temperatuur}
# new_df = pd.DataFrame([new_row])
# df = pd.concat([df, new_df], ignore_index=True)
# --------------------------------------------------------------------

# Salvestame uuendatud andmed tagasi
df.to_csv(DATA_FILE, index=False)
print("Andmed salvestatud. Kokku ridu:", len(df))

# 2. Joonistame graafiku
plt.figure(figsize=(12, 6))

# Peamine plot
plt.plot(
    df["datetime"],
    df["temperature"],
    marker="o",
    markersize=4,
    linestyle="-",
    linewidth=1.5,
    color="#1f77b4",
    label="Õhutemperatuur"
)

# X-telje formaatimine (väga oluline!)
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m %H:%M"))
ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=15))
plt.xticks(rotation=45, ha="right")

# Lisad
plt.title("Valga õhutemperatuur (automaatne uuendus)", fontsize=14, pad=15)
plt.xlabel("Aeg", fontsize=12)
plt.ylabel("Temperatuur °C", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(loc="upper left")

# Piirangud, et graafik ei veniks liiga pikaks (nt viimased 7 päeva)
if len(df) > 0:
    start_time = df["datetime"].max() - pd.Timedelta(days=7)
    plt.xlim(left=start_time)

plt.tight_layout()

# Salvestame pildi
plt.savefig(PLOT_FILE, dpi=120, bbox_inches="tight")
print("Graafik salvestatud:", PLOT_FILE)

# Lõpetame (matplotlibi jaoks hea tava Actionsis)
plt.close("all")
