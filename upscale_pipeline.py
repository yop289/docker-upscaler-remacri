from pathlib import Path
import os
import time
import cv2
from realesrgan import RealESRGANer

INPUT_DIR = Path('/gdrive/colab4x/input')
OUTPUT_DIR = Path('/gdrive/colab4x/output')
MODEL_PATH = Path('/app/models/4x_foolhardy_Remacri.pth')

# Crear carpetas por si no existen
for d in [INPUT_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

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