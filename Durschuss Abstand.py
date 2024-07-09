#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:36:37 2024

@author: marcericmitzscherling
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

# CSV-Datei einlesen
df = pd.read_csv('durchschuss.csv', delimiter=';', decimal=',')

# Einstellungen für die Farbskala
custom_colors = ['#e0d4b1', '#ebb500', '#d69c00', '#bf8400', '#a86d00', '#915700', '#784200']
custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', custom_colors)

# Einstellungen für den Graphen
fig, ax = plt.subplots(figsize=(15, 6))

# Achsenbeschriftungen und -grenzen
ax.set_xlabel('Seitenzahl')
ax.set_ylabel('Buch')
ax.set_xlim(0, 370)
ax.set_ylim(0.5, 6.5)
ax.set_yticks([1, 2, 3, 4, 5, 6])
ax.set_yticklabels(['Buch 1', 'Buch 2', 'Buch 3', 'Buch 4', 'Buch 5', 'Buch 6'])

# Einstellungen für die Farbskala
norm = mcolors.Normalize(vmin=df['qm'].min(), vmax=df['qm'].max())
scalar_map = plt.cm.ScalarMappable(norm=norm, cmap=custom_cmap)

# Rechtecke für jeden Durchschuss zeichnen
for index, row in df.iterrows():
    book = row['book']
    page = row['page']
    name = row['name']
    qm = row['qm']
    
    # Standard-Einstellungen für das Rechteck
    rect_kwargs = {
        'xy': (page-0.4, book-0.4),
        'width': 0.8,
        'height': 0.8,
        'linewidth': 0.8,
        'edgecolor': '#999999',  # Rahmenfarbe standardmäßig auf #D00B33
        'facecolor': '#999999'      # Standardmäßig keine Füllfarbe
    }
    
    # Prüfen, ob die Annotation nicht null ist
    if pd.notnull(qm):
        # Wenn qm nicht null ist, Rahmen und Füllfarbe basierend auf 'qm' festlegen
        if qm > 0:
            rect_kwargs['edgecolor'] = scalar_map.to_rgba(qm)
            rect_kwargs['facecolor'] = scalar_map.to_rgba(qm)
    
    # Ein Rechteck hinzufügen (Breite und Höhe entsprechend anpassen)
    rect = mpatches.Rectangle(**rect_kwargs)
    ax.add_patch(rect)

# Differenzen zwischen v und r berechnen, dann 1 abziehen und anzeigen
for book in df['book'].unique():
    book_df = df[df['book'] == book].reset_index()
    v_indices = book_df[book_df['name'].str.endswith('v')].index
    r_indices = book_df[book_df['name'].str.endswith('r')].index
    
    for v_index in v_indices:
        # Den nächsten r-Durchschuss nach dem v-Durchschuss finden
        next_r_index = r_indices[r_indices > v_index].min()
        if not pd.isna(next_r_index):
            v_page = book_df.loc[v_index, 'page']
            r_page = book_df.loc[next_r_index, 'page']
            diff = r_page - v_page - 1
            
            # Differenz im Diagramm anzeigen
            if diff > 0:
                mid_page = (v_page + r_page) / 2
                ax.text(mid_page, book, str(diff), ha='center', va='center', fontsize=8, color='black')
            
# Farbskala anzeigen
cax = ax.imshow([[df['qm'].min(), df['qm'].max()]], cmap=custom_cmap, aspect='auto')
cbar = fig.colorbar(cax, ax=ax, orientation='vertical', pad=0.05)
cbar.set_label('Flächeninhalt in mm²', labelpad=20)

# Einbetten der Schriftarten in das SVG
plt.rcParams['svg.fonttype'] = 'none'

# Layout anpassen und SVG speichern
plt.tight_layout()
plt.savefig('durchschuss_graph.svg', format='svg')
plt.show()
