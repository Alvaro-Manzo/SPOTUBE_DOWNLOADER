"""
API REST para Spotify Downloader
Backend Flask con endpoints para descargar música
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
import sys
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
import threading
import uuid

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el frontend

# Configuración
DOWNLOADS_DIR = Path("downloads")
TEMP_DIR = Path("temp_downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Almacenar estado de descargas
downloads_status = {}


class DownloadTask:
    """Clase para manejar tareas de descarga"""

    def __init__(self, task_id, url, name, quality="high", threads=3):
        self.task_id = task_id
        self.url = url
        self.name = name
        self.quality = quality
        self.threads = threads
        self.status = "pending"
        self.progress = 0
        self.total_songs = 0
        self.downloaded_songs = 0
        self.error = None
        self.zip_path = None

    def start(self):
        """Iniciar descarga en thread separado"""
        thread = threading.Thread(target=self._download)
        thread.daemon = True
        thread.start()

    def _download(self):
        """Proceso de descarga"""
        try:
            self.status = "downloading"

            # Crear directorio temporal para esta tarea
            task_temp_dir = TEMP_DIR / self.task_id
            task_temp_dir.mkdir(exist_ok=True)

            # Mapeo de calidad
            quality_map = {"low": "128k", "medium": "192k", "high": "320k"}

            # Comando spotdl
            cmd = [
                sys.executable,
                "-m",
                "spotdl",
                self.url,
                "--output",
                str(task_temp_dir),
                "--format",
                "mp3",
                "--bitrate",
                quality_map.get(self.quality, "320k"),
                "--threads",
                str(self.threads),
            ]

            # Ejecutar descarga
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
            )

            for line in process.stdout:
                # Aquí podrías parsear el output para actualizar progreso
                if "Found" in line and "songs" in line:
                    # Ejemplo: "Found 47 songs in playlist"
                    try:
                        self.total_songs = int(line.split("Found")[1].split("songs")[0].strip())
                    except:
                        pass

            process.wait()

            # Contar archivos descargados
            mp3_files = list(task_temp_dir.glob("*.mp3"))
            self.downloaded_songs = len(mp3_files)

            if not mp3_files:
                self.status = "error"
                self.error = "No se pudo descargar ninguna canción"
                return

            # Crear ZIP
            self.status = "compressing"
            zip_name = f"{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            zip_path = DOWNLOADS_DIR / zip_name

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for mp3_file in mp3_files:
                    zipf.write(mp3_file, mp3_file.name)

            self.zip_path = str(zip_path)
            self.status = "completed"
            self.progress = 100

            # Limpiar temporal
            shutil.rmtree(task_temp_dir)

        except Exception as e:
            self.status = "error"
            self.error = str(e)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Verificar que el servidor está funcionando"""
    return jsonify({"status": "ok", "message": "Spotify Downloader API is running"})


@app.route("/api/download", methods=["POST"])
def start_download():
    """Iniciar una nueva descarga"""
    data = request.json

    url = data.get("url")
    name = data.get("name", "playlist")
    quality = data.get("quality", "high")
    threads = data.get("threads", 3)

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Crear tarea de descarga
    task_id = str(uuid.uuid4())
    task = DownloadTask(task_id, url, name, quality, threads)
    downloads_status[task_id] = task

    # Iniciar descarga
    task.start()

    return jsonify(
        {"task_id": task_id, "status": "started", "message": "Download started successfully"}
    )


@app.route("/api/status/<task_id>", methods=["GET"])
def get_status(task_id):
    """Obtener estado de una descarga"""
    task = downloads_status.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(
        {
            "task_id": task.task_id,
            "status": task.status,
            "progress": task.progress,
            "total_songs": task.total_songs,
            "downloaded_songs": task.downloaded_songs,
            "error": task.error,
            "zip_available": task.zip_path is not None,
        }
    )


@app.route("/api/download/<task_id>", methods=["GET"])
def download_file(task_id):
    """Descargar el archivo ZIP resultante"""
    task = downloads_status.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if task.status != "completed":
        return jsonify({"error": "Download not completed yet"}), 400

    if not task.zip_path or not os.path.exists(task.zip_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(
        task.zip_path, as_attachment=True, download_name=os.path.basename(task.zip_path)
    )


@app.route("/api/downloads", methods=["GET"])
def list_downloads():
    """Listar todas las descargas"""
    result = []
    for task_id, task in downloads_status.items():
        result.append(
            {
                "task_id": task.task_id,
                "name": task.name,
                "status": task.status,
                "downloaded_songs": task.downloaded_songs,
                "total_songs": task.total_songs,
            }
        )

    return jsonify(result)


if __name__ == "__main__":
    print("🚀 Spotify Downloader API")
    print("=" * 50)
    print("Server running on: http://localhost:5001")
    print("API Health: http://localhost:5001/api/health")
    print("=" * 50)

    app.run(debug=True, host="0.0.0.0", port=5001)
