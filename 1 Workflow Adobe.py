#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:08:39 2024

@author: marcericmitzscherling
"""

import fitz  # PyMuPDF
import pandas as pd

def extract_page_heights(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page_heights = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        rect = page.rect
        page_heights.append(rect.height)
    return page_heights

def convert_coordinates(page_heights, original_y, page_number):
    page_number = int(page_number)  # Sicherstellen, dass die Seitenzahl ein Integer ist
    page_height = page_heights[page_number - 1]  # Seitenzahl ist 1-basiert
    return page_height - original_y

def process_csv_and_convert_coordinates(csv_path, pdf_path, output_csv_path):
    # Lese die CSV-Datei ein und konvertiere Komma-Zahlen in Punkt-Zahlen
    df = pd.read_csv(csv_path, delimiter=';', converters={
        'y_old_top': lambda x: float(x.replace(',', '.')),
        'y_old_sub': lambda x: float(x.replace(',', '.'))
    })
    
    # Extrahiere die Seitenhöhen aus dem PDF-Dokument
    page_heights = extract_page_heights(pdf_path)
    
    # Füge neue Spalten mit den umgekehrten y-Koordinaten hinzu
    df['Umgerechneter_y'] = df.apply(
        lambda row: convert_coordinates(page_heights, row['y_old_top'], row['page']),
        axis=1
    )
    df['Umgerechneter_y_old_sub'] = df.apply(
        lambda row: convert_coordinates(page_heights, row['y_old_sub'], row['page']),
        axis=1
    )
    
    # Speichere die Ergebnisse in einer neuen CSV-Datei, konvertiere Punkt-Zahlen zurück in Komma-Zahlen
    df['y_old_top'] = df['y_old_top'].astype(str).str.replace('.', ',')
    df['y_old_sub'] = df['y_old_sub'].astype(str).str.replace('.', ',')
    df['Umgerechneter_y'] = df['Umgerechneter_y'].astype(str).str.replace('.', ',')
    df['Umgerechneter_y_old_sub'] = df['Umgerechneter_y_old_sub'].astype(str).str.replace('.', ',')
    df.to_csv(output_csv_path, sep=';', index=False)

# Beispielnutzung:
csv_path = "koordinaten.csv"
pdf_path = "6 Om Misgierninger.pdf"
output_csv_path = "umgekehrte_koordinaten.csv"
process_csv_and_convert_coordinates(csv_path, pdf_path, output_csv_path)

print("Die umgekehrten y-Koordinaten wurden in die Datei 'umgekehrte_koordinaten.csv' geschrieben.")
