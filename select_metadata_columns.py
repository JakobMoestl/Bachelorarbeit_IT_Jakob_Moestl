import pandas as pd
import tkinter as tk
from tkinter import filedialog

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def process_file():
    input_csv_file = file_entry.get()
    if input_csv_file:
        # Pfad für die bereinigte Datei generieren
        output_csv_file = input_csv_file.replace('.csv', '_cleaned.csv')

        # CSV-Datei einlesen
        df = pd.read_csv(input_csv_file)

        # Gewünschte Spalten auswählen (nur vorhandene Spalten werden berücksichtigt)
        desired_columns = [col for col in ['/Author', '/Creator', '/CreationDate', '/ModDate', '/Producer'] if col in df.columns]

        # Wenn keine der gewünschten Spalten im DataFrame vorhanden ist
        if not desired_columns:
            print("Keine der gewünschten Spalten im CSV-Datei gefunden.")
            return

        # DataFrame auf die gewünschten Spalten reduzieren
        df = df[desired_columns]

        # Spalten in gewünschter Reihenfolge anordnen
        df = df[['/Author', '/Creator', '/CreationDate', '/ModDate', '/Producer']]

        # In ein neues CSV-Datei speichern
        df.to_csv(output_csv_file, index=False)

        print("Die bereinigten Daten wurden erfolgreich in '{}' gespeichert.".format(output_csv_file))
    else:
        print("Bitte wählen Sie eine CSV-Datei aus.")


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
# Button zum Verarbeiten der Datei
process_button = tk.Button(root, text="Datei verarbeiten", command=process_file)
process_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
