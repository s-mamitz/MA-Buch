#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 13:37:55 2024

@author: marcericmitzscherling
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Konstanten
COLOR = '#F4C000'
ALPHA = 0.05
EDGE_COLOR = '#F4C000'
LINE_WIDTH = 10.0

# CSV-Dateien laden mit spezifiziertem Trennzeichen und Dezimalzeichen
df1 = pd.read_csv('tab1.csv', delimiter=';', decimal=',')
df2 = pd.read_csv('tab2.csv', delimiter=';', decimal=',')

# Zusätzliche Spalte mit dem ersten Zeichen der ID hinzufügen
df1['ID_first_char'] = df1['ID'].str[0]
df2['ID_first_char'] = df2['ID'].str[0]

# Tabellen zusammenführen auf Basis von page und dem ersten Zeichen der ID
merged_df = pd.merge(df1, df2, on=['page', 'ID_first_char'])

# Daten nach Orientierung filtern
df_r = merged_df[merged_df['orientation'] == 'r']
df_v = merged_df[merged_df['orientation'] == 'v']

# Funktion zum Zeichnen der Rechtecke
def plot_rectangles(ax, df):
    if df.empty:
        return  # Wenn der DataFrame leer ist, nichts zeichnen

    for _, row in df.iterrows():
        rect = patches.Rectangle(
            (row['x_left_top'], row['y_left_top']),
            row['x_right_bottom'] - row['x_left_top'],
            row['y_right_bottom'] - row['y_left_top'],
            linewidth=LINE_WIDTH,
            edgecolor=EDGE_COLOR,
            facecolor='none',
            alpha=ALPHA
        )
        ax.add_patch(rect)
    
    x_min, x_max = df['x_left_top'].min(), df['x_right_bottom'].max()
    y_min, y_max = df['y_left_top'].min(), df['y_right_bottom'].max()

    if pd.notna(x_min) and pd.notna(x_max) and pd.notna(y_min) and pd.notna(y_max):
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        ax.set_aspect('equal', adjustable='box')

# Diagramme erstellen
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# Diagramm für 'r' zeichnen
plot_rectangles(ax1, df_r)
ax1.set_title('Orientation: r')

# Diagramm für 'v' zeichnen
plot_rectangles(ax2, df_v)
ax2.set_title('Orientation: v')

# Layout anpassen
plt.tight_layout()

# Einbetten der Schriftarten in das SVG
plt.rcParams['svg.fonttype'] = 'none'

# Diagramme als SVG speichern
plt.savefig('rectangles.svg', format='svg')

plt.show()
