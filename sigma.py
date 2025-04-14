import os
import subprocess
import requests
from zipfile import ZipFile

# Basis-URL des GitHub-Repos, in dem alle Pakete liegen
REPO_URL = "https://github.com/Lominub44/SigmaOS"
PACKAGES_DIR = "packages"

# Funktion zum Auflisten der Pakete im Repo (ligma list)
def list_packages():
    response = requests.get(f"{REPO_URL}/contents/")
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if item["type"] == "dir":  # Nur Ordner anzeigen
                print(item["name"])
    else:
        print("Fehler beim Abrufen der Repos.")

# Funktion zum Installieren eines Pakets (ligma install <paket>)
def download_package(package_name):
    # Ensure the "packages" directory exists
    if not os.path.exists(PACKAGES_DIR):
        os.makedirs(PACKAGES_DIR)  # Create the directory if it doesn't exist

    package_dir = os.path.join(PACKAGES_DIR, package_name)

    # If the package already exists, skip downloading
    if os.path.exists(package_dir):
        print(f"Paket {package_name} bereits heruntergeladen.")
        return

    # GitHub API URL to fetch the package directory contents
    download_url = f"{REPO_URL}/archive/refs/heads/main.zip"

    # Download the package ZIP
    print(f"Lade {package_name} herunter...")
    zip_path = os.path.join(PACKAGES_DIR, f"{package_name}.zip")
    response = requests.get(download_url)

    if response.status_code == 200:
        # Save the ZIP file locally
        with open(zip_path, "wb") as f:
            f.write(response.content)

        # Extract the ZIP archive
        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(PACKAGES_DIR)

        os.remove(zip_path)  # Delete the ZIP file after extraction

        # Locate the specific package folder in the extracted files
        extracted_folder = os.path.join(PACKAGES_DIR, "SigmaOS-main", package_name)
        if os.path.exists(extracted_folder):
            os.rename(extracted_folder, package_dir)  # Rename the folder if necessary
            print(f"Paket {package_name} erfolgreich installiert.")
        else:
            print(f"Das Paket {package_name} wurde nicht im heruntergeladenen Archiv gefunden.")
    else:
        print(f"Fehler beim Herunterladen des Pakets {package_name}.")

# Funktion zum Ausführen eines Pakets (ligma <paket>)
def run_package(package_name):
    package_dir = os.path.join(PACKAGES_DIR, package_name, "main.py")

    if not os.path.exists(package_dir):
        print(f"main.py in {package_name} nicht gefunden.")
        return

    print(f"Führe {package_name}/main.py aus...")
    subprocess.run(["python", package_dir])

# Funktion für die interaktive Kommandozeile von SigmaOS
def interactive_shell():
    while True:
        try:
            # Benutzer nach einem Befehl fragen
            command = input("SigmaOS > ")

            # Wenn der Benutzer "exit" eingibt, die Shell beenden
            if command.lower() == "exit":
                print("Beende SigmaOS...")
                break

            # Zerlege den Befehl in das Hauptkommando und mögliche Argumente
            parts = command.split()

            if not parts:
                continue

            main_command = parts[0]
            args = parts[1:]

            # Verarbeite die verschiedenen Befehle
            if main_command == "ligma":
                if args:
                    subcommand = args[0]
                    if subcommand == "list":
                        list_packages()
                    elif subcommand == "install" and len(args) == 2:
                        download_package(args[1])
                    elif len(args) == 1:
                        run_package(args[0])
                    else:
                        print("Unbekannter Befehl für ligma.")
                else:
                    print("Verwendung von ligma: list | install <paket> | <paket>")
            
            elif main_command == "delta":
                delta_command(args)
            
            else:
                print(f"Unbekannter Befehl: {main_command}. Versuche 'ligma' oder 'delta'.")

        except KeyboardInterrupt:
            print("\nBeende SigmaOS...")
            break

# Hauptfunktion, um SigmaOS zu starten
if __name__ == "__main__":
    interactive_shell()
