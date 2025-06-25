#!/bin/bash

echo "Montando Google Drive..."
mkdir -p /gdrive
rclone mount gdrive: /gdrive --vfs-cache-mode writes &

echo "Esperando 10 segundos para el montaje..."
sleep 10

echo "Iniciando procesamiento automático..."
python3 upscale_pipeline.py