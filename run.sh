# [2] run.sh (monta rclone y lanza watchdog)
#!/bin/bash

# Nombre del remote (puede ajustarse con una variable de entorno)
REMOTE_NAME=${REMOTE_NAME:-gdrive}

# Montar Google Drive
mkdir -p /gdrive
rclone mount "$REMOTE_NAME": /gdrive --vfs-cache-mode writes &

echo "[INFO] Esperando 10s para montar Google Drive..."
sleep 10

# Lanzar watchdog (procesamiento automático)
echo "[INFO] Iniciando proceso automático con ComfyUI + Remacri"
cd /workspace/ComfyUI
source venv/bin/activate
python /workspace/watchdog.py