#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:27:56 2024

@author: marcericmitzscherling
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import ScalarFormatter

# Parameter
filename = 'final.csv'  # CSV-Datei
output_image = 'heatmap.svg'  # Ausgabe Bild
output_csv = 'heatmap_data.csv'  # Ausgabe CSV
interval = 5  # Beschriftungsintervall der X-Achse
threshold_value = 25000  # Schwellenwert für Markierung
max_value_for_color_scale = 35000  # Maximalwert für die Farbskala

# Definiere eigene Bezeichnungen für die Spalten
column_names = {
    'page': 'Digitalisierung',
    'name': 'Buch',
    'summe_qm': 'Gesamtfläche',
    'art': 'Artikel',
    'pre_art': 'Artikelteile'
}

# Daten einlesen
df = pd.read_csv(filename, sep=';', decimal=',')

# Index-Spalte hinzufügen
df.insert(0, 'index', range(1, len(df) + 1))

# Sicherstellen, dass 'summe_qm' numerisch ist
df['summe_qm'] = pd.to_numeric(df['summe_qm'], errors='coerce')

# Markierte Einträge über Schwellenwert identifizieren
marked_entries = df[df['summe_qm'] > threshold_value]

# Daten für die Beschriftungspunkte vorbereiten
annotations_data = marked_entries[['page', 'name', 'summe_qm', 'art', 'pre_art']].copy()
annotations_data.reset_index(drop=True, inplace=True)
annotations_data.insert(0, 'Nummer', np.arange(1, len(annotations_data) + 1))

# Kommas als Dezimaltrennzeichen in der 'summe_qm'-Spalte verwenden
annotations_data['summe_qm'] = annotations_data['summe_qm'].apply(lambda x: f"{x:.2f}".replace('.', ','))

# Kommas in der 'art'-Spalte durch Komma und Leerzeichen ersetzen
annotations_data['art'] = annotations_data['art'].fillna('').str.replace(',', ', ')

# Leere Werte in der 'pre_art'-Spalte behandeln (keine "NaN")
annotations_data['pre_art'] = annotations_data['pre_art'].fillna('').str.replace(',', ', ')

# CSV-Datei für die Beschriftungspunkte speichern
annotations_data.to_csv(output_csv, index=False, sep=';', decimal=',')

# Heatmap-Daten vorbereiten
heatmap_data = df[['index', 'summe_qm']].set_index('index').T

#Eigene Farben 
custom_colors = ['#ffffff', '#e0d4b1', '#ebb500', '#d69c00', '#bf8400', '#a86d00', '#915700', '#784200']
custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', custom_colors)

# Heatmap erstellen
fig, ax = plt.subplots(figsize=(10, 6))
cax = ax.imshow(heatmap_data, cmap=custom_cmap, aspect='auto', vmin=0, vmax=max_value_for_color_scale)

# X-Achse anpassen
ax.set_xticks(np.arange(0, len(df), interval))
ax.set_xticklabels(df['name'][::interval], rotation=90)

# Y-Achse anpassen
ax.set_yticks([])  # keine Y-Achsenbeschriftung

# Farblegende hinzufügen
cbar = fig.colorbar(cax, orientation='vertical')
cbar.set_label('Flächeninhalt in mm²', labelpad=20)

# Skalierung der Farblegende auf tatsächliche Werte anpassen
formatter = ScalarFormatter(useOffset=False)
formatter.set_scientific(False)
cbar.ax.yaxis.set_major_formatter(formatter)

# Markierte Punkte in der Heatmap einfügen
y_position = 0

for i, (index, row) in enumerate(marked_entries.iterrows()):
    if i % 2 == 0:
        y_position -= 0.02  # Verschiebe die y-Position nach unten um 0.5 Einheiten für jedes gerade Label
    else:
        y_position -= 0.02  # Verschiebe die y-Position nach unten um 1.0 Einheiten für jedes ungerade Label

    ax.plot(index - 1, y_position, marker='s', markersize=5, color='black')  # Platziere ein Quadrat

    ax.text(index, y_position, str(i + 1), ha='left', va='center', color='black', fontsize=10)  # Platziere den Text rechts neben dem Quadrat

# Einbetten der Schriftarten in das SVG
plt.rcParams['svg.fonttype'] = 'none'

# Speichern der Heatmap als SVG
plt.tight_layout()
plt.savefig('heatmap.svg', format='svg', dpi=1200, bbox_inches='tight', transparent=True)

plt.show()
