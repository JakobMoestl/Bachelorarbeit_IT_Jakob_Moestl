import pandas as pd

# Dateipfad zur CSV-Datei
input_csv_file = r"C:\Users\Jakob Moestl\Documents\Studium\PBIT_SS2024\SynologyDrive\Bachelorarbeit\Metadaten\metadatenfhbfi.csv"

# Dateipfad für das neue CSV-Datei
output_csv_file = r"C:\Users\Jakob Moestl\Documents\Studium\PBIT_SS2024\SynologyDrive\Bachelorarbeit\Metadaten\metadatenfhbfi2.csv"


# Spalten, die behalten werden sollen
desired_columns = ['/Author', '/Creator', '/CreationDate', '/ModDate', '/Producer']

# CSV-Datei einlesen
df = pd.read_csv(input_csv_file)

# Nicht benötigte Spalten droppen
df = df[desired_columns]

# In ein neues CSV-Datei speichern
df.to_csv(output_csv_file, index=False)

print("Die bereinigten Daten wurden erfolgreich in '{}' gespeichert.".format(output_csv_file))
