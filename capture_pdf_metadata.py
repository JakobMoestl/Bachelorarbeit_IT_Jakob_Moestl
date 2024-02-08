import os
import logging
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from PyPDF2 import PdfReader

# Konfiguriere das Logging
logging.basicConfig(filename='logfile.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Setze den ausgewählten Ordner im Eingabefeld
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

def process_folder():
    pdf_dir = folder_entry.get()
    if os.path.isdir(pdf_dir):
        # Übergeordneter Ordnername
        parent_folder = os.path.basename(os.path.normpath(pdf_dir))
        # Liste für die Metadaten
        metadata_list = []
        # Durchlauf aller PDF-Dateien im Verzeichnis
        for filename in os.listdir(pdf_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(pdf_dir, filename)
                try:
                    # PDF-Datei lesen
                    with open(pdf_path, 'rb') as f:
                        pdf = PdfReader(f)
                        # Metadaten extrahieren
                        metadata = pdf.metadata
                        if metadata is not None:
                            metadata_list.append(metadata)
                        else:
                            logging.warning(f'Keine Metadaten gefunden: {filename}')
                except Exception as e:
                    logging.error(f'Fehler beim Lesen der Datei {filename}: {e}')

        # Metadaten in ein DataFrame konvertieren
        df = pd.DataFrame(metadata_list)

        # Speicherort der CSV-Datei auf deinem Desktop
        csv_file = os.path.join(pdf_dir, f'{parent_folder}_metadata.csv')

        # DataFrame in eine CSV-Datei exportieren
        df.to_csv(csv_file, index=False)

        print("Metadaten wurden erfolgreich in '{}' gespeichert.".format(csv_file))
    else:
        logging.error('Ungültiger Ordnerpfad.')

# GUI erstellen
root = tk.Tk()
root.title("PDF Metadata Extraction")

# Label und Eingabefeld für den Ordnerpfad
folder_label = tk.Label(root, text="PDF-Ordner auswählen:")
folder_label.grid(row=0, column=0, padx=10, pady=10)
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=10, pady=10)
# Button zum Auswählen des Ordners
select_button = tk.Button(root, text="Ordner auswählen", command=select_folder)
select_button.grid(row=0, column=2, padx=10, pady=10)
# Button zum Verarbeiten des Ordners
process_button = tk.Button(root, text="Ordner verarbeiten", command=process_folder)
process_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
