#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 18:44:39 2024

@author: marcericmitzscherling
"""

import pandas as pd

# CSV-Dateien einlesen
tab1 = pd.read_csv('tab1.csv', delimiter=';', decimal=',')
tab2 = pd.read_csv('tab2.csv', delimiter=';', decimal=',')
tab4 = pd.read_csv('tab4.csv', delimiter=';', decimal=',')

# Schritt 1: Summe der Flächeninhalte pro Seite in tab2.csv berechnen
sum_qm_per_page = tab2.groupby('page')['qm'].sum().reset_index()
sum_qm_per_page.columns = ['page', 'summe_qm']

# Schritt 2: Summen in tab4.csv einfügen und leere Zellen mit 0 auffüllen
tab4 = tab4.merge(sum_qm_per_page, on='page', how='left')
tab4['summe_qm'] = tab4['summe_qm'].fillna(0)
tab4['summe_qm'] = tab4['summe_qm'].round(2)

#Schritt 3: Artikel ergänzen
# Funktion zur Überprüfung des Formats 'Zahlen-Zahlen-Zahlen'
def check_item_format(item):
    parts = item.split('-')
    if len(parts) == 3:
        for part in parts:
            if not part.isdigit():
                return False
        return True
    return False

# Artikel aus tab1.csv extrahieren, deren item dem Schema 'Zahlen-Zahlen-Zahlen' entspricht
articles_tab1 = tab1[tab1['item'].apply(check_item_format)]

# Funktion zum Extrahieren der Artikel pro Seite aus tab1.csv
def get_articles_for_page(page):
    articles = articles_tab1[articles_tab1['page'] == page]['item'].tolist()
    return articles

# Sicherstellen, dass 'art'-Spalte in tab4 vorhanden ist oder erstellt wird
if 'art' not in tab4.columns:
    tab4['art'] = ''

# Artikel pro Seite in tab4.csv hinzufügen
for index, row in tab4.iterrows():
    page = row['page']
    current_articles = get_articles_for_page(page)
    if current_articles:
        articles_str = ','.join(current_articles)
        tab4.at[index, 'art'] = articles_str

# Leere Zellen in der Spalte 'art' mit '' (leerem String) ersetzen
tab4['art'] = tab4['art'].fillna('')

# Ergebnis als CSV speichern
tab4.to_csv('tab4_art.csv', sep=';', decimal=',', index=False)

print(tab4.head())