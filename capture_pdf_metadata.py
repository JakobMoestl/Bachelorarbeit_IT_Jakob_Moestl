import os
import logging
import pandas as pd
from PyPDF2 import PdfReader

# Konfiguriere das Logging
logging.basicConfig(filename='logfile.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Verzeichnis mit den PDF-Dateien
pdf_dir = r'C:\Users\jakob\Desktop\FHBFI PDF'

# Liste für die Metadaten
metadata_list = []

# Durchlauf aller PDF-Dateien im Verzeichnis
for filename in os.listdir(pdf_dir):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, filename)
        if filename.endswith('.pdf'):
            print(filename)
            # PDF-Datei lesen
            with open(pdf_path, 'rb') as f:
                pdf = PdfReader(f)
                # Metadaten extrahieren
                metadata = pdf.metadata
                print(metadata)
                metadata_list.append(metadata)

# Metadaten in ein DataFrame konvertieren
df = pd.DataFrame(metadata_list)

# Speicherort der CSV-Datei auf deinem Desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
csv_file = os.path.join(desktop_path, 'metadaten.csv')

# DataFrame in eine CSV-Datei exportieren
df.to_csv(csv_file, index=False)

print("Metadaten wurden erfolgreich in '{}' gespeichert.".format(csv_file))
