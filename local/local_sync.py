import os
import time
import shutil
import rclone
from pathlib import Path

LOCAL_INPUT = Path("./local_input")
LOCAL_OUTPUT = Path("./local_output")
REMOTE_INPUT = "gdrive:colab4x/input"
REMOTE_OUTPUT = "gdrive:colab4x/output"

# Crear carpetas locales si no existen
LOCAL_INPUT.mkdir(parents=True, exist_ok=True)
LOCAL_OUTPUT.mkdir(parents=True, exist_ok=True)

# Subir todas las imágenes nuevas desde local_input
for file in LOCAL_INPUT.glob("*.png"):
    print(f"[⬆️] Subiendo {file.name} a Drive...")
    os.system(f"rclone copy '{file}' {REMOTE_INPUT}")

# Esperar y descargar procesadas
print("[⏳] Esperando resultados...")
while True:
    os.system(f"rclone ls {REMOTE_OUTPUT} > output_list.txt")
    with open("output_list.txt", "r") as f:
        lines = f.readlines()

    found = False
    for line in lines:
        if line.strip():
            size, name = line.strip().split(None, 1)
            remote_file = f"{REMOTE_OUTPUT}/{name}"
            local_path = LOCAL_OUTPUT / name
            print(f"[⬇️] Descargando {name}...")
            os.system(f"rclone copy '{remote_file}' '{LOCAL_OUTPUT}'")
            os.system(f"rclone delete '{remote_file}'")
            found = True

    if found:
        print("[✅] Resultado descargado. Puedes revisar local_output/")
        break

    time.sleep(5)
