#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:00:18 2024

@author: marcericmitzscherling
"""

import pandas as pd

# CSV-Dateien einlesen
tab3 = pd.read_csv('tab3.csv', sep=';', decimal=',')
tab4 = pd.read_csv('tab4_art_preart.csv', sep=';', decimal=',')

# Füge eine neue Spalte zum Markieren der zu löschenden Zeilen hinzu
tab4['to_delete'] = False

# Durchlaufen der Seiten in tab3
for index, row in tab3.iterrows():
    page = row['page']
    orientation = row['orientation']

    if page in tab4['page'].values:
        tab4_index = tab4.index[tab4['page'] == page].tolist()[0]

        if orientation == 'r' and tab4_index > 0:
            tab4.at[tab4_index - 1, 'summe_qm'] += float(tab4.at[tab4_index, 'summe_qm'])
            tab4.at[tab4_index, 'to_delete'] = True  # Markiere die bearbeitete Zeile
        elif orientation == 'v' and tab4_index < len(tab4) - 1:
            tab4.at[tab4_index + 1, 'summe_qm'] += float(tab4.at[tab4_index, 'summe_qm'])
            tab4.at[tab4_index, 'to_delete'] = True  # Markiere die bearbeitete Zeile

# Löschen der Zeilen, die markiert wurden
tab4 = tab4[tab4['to_delete'] == False]

#Werte in summe_qm wieder auf 2 Stellen runden
tab4['summe_qm'] = tab4['summe_qm'].round(2)

# Entferne die 'to_delete' Spalte
tab4.drop(columns=['to_delete'], inplace=True)

# Index neu setzen und CSV speichern
tab4.reset_index(drop=True, inplace=True)
tab4.to_csv('final.csv', sep=';', decimal=',', index=False)

print("Das Ergebnis wurde in final.csv gespeichert.")
