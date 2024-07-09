#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:24:30 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Lese tab1.csv ein und filtere nach Zeilen, deren item-Wert mit einer Zahl beginnt
tab1 = pd.read_csv('tab1.csv', sep=';', decimal=',')
tab1 = tab1[tab1['item'].str.match(r'^\d+.*', na=False)]

# Lese tab4.csv ein
tab4 = pd.read_csv('tab4_art.csv', sep=';', decimal=',')

# Funktion zur Verarbeitung einer Seite in tab4.csv
def process_page(page_number):
    if page_number in tab1['page'].values:
        # Filtere tab1 nach der aktuellen page_number
        relevant_pages = tab1[tab1['page'] == page_number]
        
        if len(relevant_pages) > 1:
            # Es gibt mehrere Treffer in tab1.csv für diese Seite, wähle den höchsten y-Wert
            max_y_page = relevant_pages.loc[relevant_pages['y'].idxmax()]
            if max_y_page['y'] < 500:
                if str(max_y_page['item']).endswith("-1"):
                    if max_y_page['y'] < 300:
                        # Verwende die vorherige Zeile in tab1.csv
                        preceding_row_index = tab1.index.get_loc(max_y_page.name) - 1
                        if preceding_row_index >= 0:
                            preceding_row = tab1.iloc[preceding_row_index]
                            return preceding_row['item']
                else:
                    # Ganz normal im Script fortfahren und den item der vorherigen Zeile speichern
                    preceding_row_index = tab1.index.get_loc(max_y_page.name) - 1
                    if preceding_row_index >= 0:
                        preceding_row = tab1.iloc[preceding_row_index]
                        return preceding_row['item']

        
        elif len(relevant_pages) == 1:
            # Es gibt nur einen Treffer für diese Seite in tab1.csv
            page_row = relevant_pages.iloc[0]
            if page_row['y'] < 500:
                if str(page_row['item']).endswith("-1"):
                    if page_row['y'] < 300:
                        # Verwende die vorherige Zeile in tab1.csv
                        preceding_row_index = tab1.index.get_loc(page_row.name) - 1
                        if preceding_row_index >= 0:
                            preceding_row = tab1.iloc[preceding_row_index]
                            return preceding_row['item']
                else:
                    # Ganz normal im Script fortfahren und den item der vorherigen Zeile speichern
                    preceding_row_index = tab1.index.get_loc(page_row.name) - 1
                    if preceding_row_index >= 0:
                        preceding_row = tab1.iloc[preceding_row_index]
                        return preceding_row['item']

    
    return None

# Für jede Seite in tab4.csv überprüfen und neuen item-Namen einfügen
for idx, row in tab4.iterrows():
    page_number = row['page']
    new_item_name = process_page(page_number)
    if new_item_name is not None:
        # Füge den neuen item-Namen in eine neue Spalte am Ende von tab4.csv ein
        tab4.loc[idx, 'pre_art'] = new_item_name

# Speichere das Ergebnis als tab4_neu_neu.csv
tab4.to_csv('tab4_art_preart.csv', sep=';', decimal=',', index=False)