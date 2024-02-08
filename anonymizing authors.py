import os
import pandas as pd
import random
import string

# Funktion zur Anonymisierung eines Autorennamens
def anonymize_author(author, mapping_dict):
    if author in mapping_dict:
        return mapping_dict[author]
    else:
        pseudonym = ''.join(random.choices(string.ascii_lowercase, k=5))
        mapping_dict[author] = pseudonym
        return pseudonym

# Pfad zur CSV-Datei mit den Originaldaten
input_csv_file = r"C:\Users\Jakob Moestl\Desktop\FHBFI PDF\FHBFI PDF_metadata.csv"

# Einlesen der CSV-Datei
df = pd.read_csv(input_csv_file)

# Laden der vorhandenen Zuordnungsinformationen, falls vorhanden
mapping_csv_file = "mapping_data.csv"
mapping_dict = {}
if os.path.exists(mapping_csv_file):
    mapping_df = pd.read_csv(mapping_csv_file)
    mapping_dict = dict(zip(mapping_df['/Author'], mapping_df['Anonymized_Author']))

# Anonymisierung der Autorenspalte
df['Anonymized_Author'] = df['/Author'].apply(lambda x: anonymize_author(x, mapping_dict))

# Droppen der Spalte /Author
df.drop('/Author', axis=1, inplace=True)

# Pfad zum Desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

# Generieren des Dateinamens für die anonymisierte CSV-Datei
output_csv_file = os.path.join(desktop_path, "anonymized_data_" + ''.join(random.choices(string.ascii_lowercase, k=5)) + ".csv")

# Schreiben der anonymisierten Daten in die CSV-Datei
df.to_csv(output_csv_file, index=False)

# Generieren des Dateinamens für die Mapping-CSV-Datei
mapping_csv_file = os.path.join(desktop_path, "mapping_data_" + ''.join(random.choices(string.ascii_lowercase, k=5)) + ".csv")

# Erzeugen einer Zuordnungstabelle für den Rückbezug zu den ursprünglichen Daten
mapping_df = pd.DataFrame(list(mapping_dict.items()), columns=['/Author', 'Anonymized_Author'])

# Schreiben der Zuordnungsinformationen in eine separate CSV-Datei
mapping_df.to_csv(mapping_csv_file, index=False)

print("Anonymisierte Daten wurden erfolgreich gespeichert in '{}'.".format(output_csv_file))
print("Zuordnungsinformationen wurden erfolgreich gespeichert in '{}'.".format(mapping_csv_file))
