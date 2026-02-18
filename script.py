import requests
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# URL XML-andmetega
url = 'https://www.ilmateenistus.ee/ilma_andmed/xml/observations.php'

# Hangi andmed
response = requests.get(url)
tree = ET.fromstring(response.content)

# Ajatempel (Unix timestamp)
timestamp = int(tree.attrib['timestamp'])
dt = datetime.fromtimestamp(timestamp)

# Leia Valga jaam
temp = None
for station in tree.findall('station'):
    name = station.find('name').text
    if name and 'Valga' in name:  # Otsi 'Valga' sisaldavat nime (nt 'Valga')
        temp_str = station.find('airtemperature').text
        if temp_str:
            temp = float(temp_str)
        break

if temp is None:
    print("Valga andmeid ei leitud!")
    exit(1)

# Lae olemasolev CSV või loo uus
if os.path.exists('data.csv'):
    df = pd.read_csv('data.csv')
else:
    df = pd.DataFrame(columns=['timestamp', 'datetime', 'temperature'])

# Lisa uus rida (väldi duplikaate, kui timestamp on sama)
if not df.empty and df['timestamp'].iloc[-1] == timestamp:
    print("Andmed juba olemas, ei lisa duplikaati.")
else:
    new_row = pd.DataFrame({'timestamp': [timestamp], 'datetime': [dt], 'temperature': [temp]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('data.csv', index=False)

# Genereeri graafik (aja vs temperatuuri)
plt.figure(figsize=(10, 5))
plt.plot(df['datetime'], df['temperature'], marker='o')
plt.title('Valga temperatuuriandmed')
plt.xlabel('Aeg')
plt.ylabel('Temperatuur (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot.png')
plt.close()
