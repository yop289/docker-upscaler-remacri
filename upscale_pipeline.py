from pathlib import Path
import os
import time
import cv2
from realesrgan import RealESRGANer

# Rutas en Drive
INPUT_DIR = Path('/gdrive/colab4x/input')
OUTPUT_DIR = Path('/gdrive/colab4x/output')
MODEL_DIR = Path('/gdrive/colab4x/models')
MODEL_PATH = MODEL_DIR / 'RealESRGAN_x4plus.pth'

# Crear directorios
for d in [INPUT_DIR, OUTPUT_DIR, MODEL_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Descargar modelo si no existe
if not MODEL_PATH.exists():
    print("Descargando modelo Remacri...")
    os.system(f"wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5/RealESRGAN_x4plus.pth -O {MODEL_PATH}")

def upscale_image(input_path, output_path):
    img = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
    upscaler = RealESRGANer(
        scale=4,
        model_path=str(MODEL_PATH),
        model=None,
        tile=512,
        tile_pad=10,
        pre_pad=0,
        half=True
    )
    output, _ = upscaler.enhance(img)
    cv2.imwrite(str(output_path), output)

def watch_and_process():
    processed = set()
    while True:
        for fname in os.listdir(INPUT_DIR):
            if fname.lower().endswith(('.png', '.jpg')) and fname not in processed:
                in_path = INPUT_DIR / fname
                out_path = OUTPUT_DIR / f"upscaled_{fname}"
                print(f"Procesando: {fname}")
                upscale_image(in_path, out_path)
                processed.add(fname)
        time.sleep(5)

if __name__ == "__main__":
    watch_and_process()