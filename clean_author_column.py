import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog

# Funktion zur Überprüfung, ob ein vollständiger Name vorhanden ist
def has_full_name(name):
    # Überprüfen, ob der Name ein String ist und nicht leer ist
    if isinstance(name, str) and name.strip():
        # Reguläre Ausdrücke für die Überprüfung eines vollständigen Namens (mindestens ein Leerzeichen, ein Komma oder ein Punkt)
        pattern_space = r'^\w+\s\w+$'  # Vorname Nachname
        pattern_comma = r'^\w+,\s\w+$'  # Nachname, Vorname
        pattern_dot = r'^\w+\.\w+$'      # Vorname.Nachname
        # Überprüfen, ob der Name einem der Muster entspricht und nicht mehr als 2 Wörter hat
        return bool(re.match(pattern_space, name)) or bool(re.match(pattern_comma, name)) or bool(re.match(pattern_dot, name))
    else:
        return False

# Funktion zur Umwandlung des Namensformats in "Nachname, Vorname"
def format_name(name):
    if has_full_name(name):
        parts = re.split(r'\s|,', name.strip())
        if len(parts) == 2:
            return parts[1] + ", " + parts[0]
        else:
            return name
    else:
        return None  # Rückgabe von None für nicht vollständige Namen

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def process_file():
    input_csv_file = file_entry.get()
    if input_csv_file:
        # Einlesen der CSV-Datei
        df = pd.read_csv(input_csv_file)

        # Bereinigung der Spalte "/Author" basierend auf dem Vollständigkeitskriterium
        df["bereinigter_Author"] = df["/Author"].fillna("").apply(lambda x: format_name(x))

        # Filtern der Datensätze mit bereinigten Autoren
        cleaned_df = df.dropna(subset=["bereinigter_Author"])

        # Überschreiben der ursprünglichen CSV-Datei
        cleaned_df.to_csv(input_csv_file, index=False)
        print("Die CSV-Datei wurde bereinigt und überschrieben.")
    else:
        print("Es wurde keine CSV-Datei ausgewählt.")

# GUI erstellen
root = tk.Tk()
root.title("CSV-Datei bereinigen")

# Label und Eingabefeld für die Dateiauswahl
file_label = tk.Label(root, text="CSV-Datei auswählen:")
file_label.grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)
# Button zum Auswählen der Datei
select_button = tk.Button(root, text="Datei auswählen", command=select_file)
select_button.grid(row=0, column=2, padx=10, pady=10)

# Button zum Verarbeiten der Datei
process_button = tk.Button(root, text="Datei verarbeiten", command=process_file)
process_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
