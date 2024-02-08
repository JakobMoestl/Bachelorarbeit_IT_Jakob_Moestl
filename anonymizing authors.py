import os
import pandas as pd
import random
import string
import tkinter as tk
from tkinter import filedialog

# Funktion zur Anonymisierung eines Autorennamens
def anonymize_author(author, mapping_dict):
    if author in mapping_dict:
        return mapping_dict[author]
    else:
        pseudonym = ''.join(random.choices(string.ascii_lowercase, k=5))
        mapping_dict[author] = pseudonym
        return pseudonym

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# GUI erstellen
root = tk.Tk()
root.title("Dateiauswahl")

# Label und Eingabefeld für die Dateiauswahl
file_label = tk.Label(root, text="CSV-Datei auswählen:")
file_label.grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)
# Button zum Auswählen der Datei
select_button = tk.Button(root, text="Datei auswählen", command=select_file)
select_button.grid(row=0, column=2, padx=10, pady=10)

def process_file():
    input_csv_file = file_entry.get()
    if os.path.exists(input_csv_file):
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

        # Pfad zur Ausgabedatei im selben Ordner wie die Eingabedatei
        output_csv_file = os.path.join(os.path.dirname(input_csv_file), "anonymized_data_" + os.path.basename(input_csv_file))

        # Schreiben der anonymisierten Daten in die CSV-Datei
        df.to_csv(output_csv_file, index=False)

        # Generieren des Dateinamens für die Mapping-CSV-Datei
        mapping_csv_file = os.path.join(os.path.dirname(input_csv_file), "mapping_data_" + ''.join(random.choices(string.ascii_lowercase, k=5)) + ".csv")

        # Erzeugen einer Zuordnungstabelle für den Rückbezug zu den ursprünglichen Daten
        mapping_df = pd.DataFrame(list(mapping_dict.items()), columns=['/Author', 'Anonymized_Author'])

        # Schreiben der Zuordnungsinformationen in eine separate CSV-Datei
        mapping_df.to_csv(mapping_csv_file, index=False)

        print("Anonymisierte Daten wurden erfolgreich gespeichert in '{}'.".format(output_csv_file))
        print("Zuordnungsinformationen wurden erfolgreich gespeichert in '{}'.".format(mapping_csv_file))
    else:
        print("Die ausgewählte Datei existiert nicht.")

# Button zum Verarbeiten der Datei
process_button = tk.Button(root, text="Datei verarbeiten", command=process_file)
process_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
