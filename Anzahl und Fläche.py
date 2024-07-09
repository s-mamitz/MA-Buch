#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 17:51:52 2024

@author: marcericmitzscherling
"""

import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei einlesen
df = pd.read_csv('annotation.csv', delimiter=';', decimal=',')

# Buchstaben und Farben zuordnen
books = ['A', 'B', 'C', 'D', 'E', 'F']
book_names = ['Buch 1', 'Buch 2', 'Buch 3', 'Buch 4', 'Buch 5', 'Buch 6']
colors = ['#e0d4b1', '#ebb500', '#d69c00', '#bf8400', '#a86d00', '#915700']

plt.figure(figsize=(14, 8))

for book, color in zip(books, colors):
    book_df = df[df['id'].str.startswith(book)]
    
    # Gruppieren nach Seitenzahl und Summen und Zählen berechnen
    sum_qm_per_page = book_df.groupby('page')['qm'].sum()
    count_annotations_per_page = book_df.groupby('page')['qm'].count()
    
    # Erstellen von Listen für die x- und y-Werte des Streudiagramms
    x_values = sum_qm_per_page.values
    y_values = count_annotations_per_page.values
    
    # Streudiagramm plotten
    plt.scatter(x_values, y_values, label=f'{book}', color=color, alpha=0.6)

plt.xlabel('Summe der Flächeninhalte der Annotationen (qm)')
plt.ylabel('Anzahl der Annotationen auf der Seite')
plt.title('Zusammenhang zwischen Flächeninhalt und Anzahl der Annotationen')
plt.legend(title='Bücher')

#Ausgabe der Extreme in der Konsole
pages_with_10_or_more_annotations = {}
for book in books:
    book_df = df[df['id'].str.startswith(book)]
    
    # Gruppieren nach Seitenzahl und Zählen der Annotationen pro Seite
    count_annotations_per_page = book_df.groupby('page')['qm'].count()
    
    # Seitenzahlen mit 10 oder mehr Annotationen filtern
    filtered_pages = count_annotations_per_page[count_annotations_per_page >= 10]
    
    if not filtered_pages.empty:
        pages_with_10_or_more_annotations[book] = filtered_pages.index.tolist()

# Ausgabe der Seitenzahlen und Bücher in der Konsole
for book, pages in pages_with_10_or_more_annotations.items():
    print(f"Buch {book}: Seitenzahlen mit 10 oder mehr Annotationen: {pages}")
    
# Einbetten der Schriftarten in das SVG
plt.rcParams['svg.fonttype'] = 'none'

# Speichern der Grafik als SVG-Datei
plt.savefig('annotation_scatter_plot.svg', format='svg')

# Anzeige der Grafik
plt.show()
