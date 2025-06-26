# [3] watchdog.py (observa Drive y lanza workflows)
import os
import time
import json
import subprocess
from pathlib import Path

INPUT_DIR = Path("/gdrive/colab4x/input")
OUTPUT_DIR = Path("/gdrive/colab4x/output")
WORKFLOW_PATH = Path("/workspace/workflows/generative_upscale.json")
QUEUE_DIR = Path("/workspace/ComfyUI/input")
RESULTS_DIR = Path("/workspace/ComfyUI/output")

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
QUEUE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

processed = set()

def run_comfy_workflow(image_path):
    workflow = json.load(open(WORKFLOW_PATH))
    for node in workflow.values():
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str) and "<INPUT>" in v:
                    node[k] = str(image_path)
    
    workflow_input = Path("/workspace/ComfyUI/input/generated_workflow.json")
    with open(workflow_input, "w") as f:
        json.dump(workflow, f, indent=2)

    subprocess.run([
        "python", "main.py",
        "--cli",
        "--workflow", str(workflow_input)
    ])

    out_image = next(RESULTS_DIR.glob("*.png"), None)
    if out_image:
        out_name = f"upscaled_{image_path.name}"
        out_dest = OUTPUT_DIR / out_name
        out_image.rename(out_dest)
        print(f"[✅] Guardado: {out_dest}")

while True:
    for fname in os.listdir(INPUT_DIR):
        if fname.endswith((".jpg", ".png")) and fname not in processed:
            in_path = INPUT_DIR / fname
            print(f"[▶️] Procesando: {fname}")
            run_comfy_workflow(in_path)
            processed.add(fname)
    time.sleep(5)