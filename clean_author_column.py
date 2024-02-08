import pandas as pd
import re

# Funktion zur Überprüfung, ob ein vollständiger Name vorhanden ist
def has_full_name(name):
    # Überprüfen, ob der Name ein String ist und nicht leer ist
    if isinstance(name, str) and name.strip():
        # Reguläre Ausdrücke für die Überprüfung eines vollständigen Namens (mindestens ein Leerzeichen oder ein Komma)
        pattern_space = r'^\w+\s\w+$'  # Vorname Nachname
        pattern_comma = r'^\w+,\s\w+$'  # Nachname, Vorname
        # Überprüfen, ob der Name einem der beiden Muster entspricht und nicht mehr als 2 Wörter hat
        return bool(re.match(pattern_space, name)) or bool(re.match(pattern_comma, name))
    else:
        return False

# Pfad zur CSV-Datei
csv_file_path = "C:\\Users\\Jakob Moestl\\Documents\\Studium\\PBIT_SS2024\\SynologyDrive\\Bachelorarbeit\\Metadaten\\metadatenfhbfi.csv"

# CSV-Datei einlesen
df = pd.read_csv(csv_file_path)

# Bereinigung der Spalte "/Author" basierend auf dem Vollständigkeitskriterium
df["bereinigter_Author"] = df["/Author"].fillna("").apply(lambda x: x if has_full_name(x) else None)

# Filtern der Datensätze mit bereinigten Autoren
cleaned_df = df.dropna(subset=["bereinigter_Author"])

# Speicherort der neuen CSV-Datei
output_csv_file_path = "C:\\Users\\Jakob Moestl\\Documents\\Studium\\PBIT_SS2024\\SynologyDrive\\Bachelorarbeit\\Metadaten\\bereinigte_metadatenfhbfi.csv"

# Speichern der bereinigten Daten in eine neue CSV-Datei
cleaned_df.to_csv(output_csv_file_path, index=False)

print("Bereinigte Daten wurden erfolgreich in '{}' gespeichert.".format(output_csv_file_path))
