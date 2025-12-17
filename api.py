"""
API REST para Spotify Downloader con Sistema de Autenticación
Backend Flask con login, registro, panel admin y sistema freemium
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os
import subprocess
import sys
import zipfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import threading
import uuid
import json
import jwt
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "tu-clave-secreta-super-segura-cambiar-en-produccion"
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

# Configuración
DOWNLOADS_DIR = Path("downloads")
TEMP_DIR = Path("temp_downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Archivos de datos
USERS_FILE = ".users_db.json"
USAGE_FILE = ".usage_limits.json"

# Límites
FREE_MONTHLY_LIMIT = 1  # 1 playlist por mes GRATIS

# Almacenar estado de descargas
downloads_status = {}


# ==================== BASE DE DATOS DE USUARIOS ====================


def load_users():
    """Carga la base de datos de usuarios."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    # Usuario admin por defecto
    admin = {
        "admin@spotube.com": {
            "password": bcrypt.generate_password_hash("admin123").decode("utf-8"),
            "is_admin": True,
            "is_pro": True,
            "created_at": datetime.now().isoformat(),
            "downloads_count": 0,
        }
    }
    save_users(admin)
    return admin


def save_users(users_data):
    """Guarda la base de datos de usuarios."""
    with open(USERS_FILE, "w") as f:
        json.dump(users_data, f, indent=2)


def load_usage(email):
    """Carga el uso de un usuario específico."""
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            data = json.load(f)
            return data.get(email, {"downloads": []})
    return {"downloads": []}


def save_usage(email, usage_data):
    """Guarda el uso de un usuario."""
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            all_usage = json.load(f)
    else:
        all_usage = {}

    all_usage[email] = usage_data

    with open(USAGE_FILE, "w") as f:
        json.dump(all_usage, f, indent=2)


# ==================== SISTEMA DE AUTENTICACIÓN ====================


def create_token(email, is_admin=False):
    """Crea un JWT token para el usuario."""
    payload = {
        "email": email,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(days=7),  # Token válido por 7 días
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def token_required(f):
    """Decorator para rutas que requieren autenticación."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Token puede venir en el header Authorization
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data["email"]
        except:
            return jsonify({"error": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    """Decorator para rutas que solo admins pueden acceder."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            if not data.get("is_admin", False):
                return jsonify({"error": "Admin access required"}), 403
            current_user = data["email"]
        except:
            return jsonify({"error": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# ==================== ENDPOINTS DE AUTENTICACIÓN ====================


@app.route("/api/auth/register", methods=["POST"])
def register():
    """Registrar nuevo usuario."""
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    users = load_users()

    if email in users:
        return jsonify({"error": "User already exists"}), 400

    # Hash de la contraseña
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Crear usuario con 7 días de prueba PRO GRATIS
    trial_end = datetime.now() + timedelta(days=7)
    users[email] = {
        "password": hashed_password,
        "name": name,
        "is_admin": False,
        "is_pro": True,  # PRO por 7 días
        "trial_end": trial_end.isoformat(),  # Fecha fin de prueba
        "created_at": datetime.now().isoformat(),
        "downloads_count": 0,
    }

    save_users(users)

    # Crear token
    token = create_token(email, False)

    return jsonify(
        {
            "message": "¡Bienvenido! Tienes 7 días de PRO GRATIS 🎉",
            "token": token,
            "user": {
                "email": email,
                "name": name,
                "is_pro": True,
                "is_admin": False,
                "trial_days_left": 7,
            },
        }
    )


@app.route("/api/auth/login", methods=["POST"])
def login():
    """Login de usuario."""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    users = load_users()

    if email not in users:
        return jsonify({"error": "Invalid credentials"}), 401

    user = users[email]

    # Verificar contraseña
    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Crear token
    token = create_token(email, user.get("is_admin", False))

    return jsonify(
        {
            "message": "Login successful",
            "token": token,
            "user": {
                "email": email,
                "name": user.get("name", ""),
                "is_pro": user.get("is_pro", False),
                "is_admin": user.get("is_admin", False),
                "downloads_count": user.get("downloads_count", 0),
            },
        }
    )


@app.route("/api/auth/me", methods=["GET"])
@token_required
def get_current_user(current_user):
    """Obtener información del usuario actual."""
    users = load_users()
    user = users.get(current_user)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(
        {
            "email": current_user,
            "name": user.get("name", ""),
            "is_pro": user.get("is_pro", False),
            "is_admin": user.get("is_admin", False),
            "downloads_count": user.get("downloads_count", 0),
            "created_at": user.get("created_at"),
        }
    )


# ==================== PANEL DE ADMINISTRACIÓN ====================


@app.route("/api/admin/users", methods=["GET"])
@admin_required
def get_all_users(current_user):
    """Obtener lista de todos los usuarios (solo admin)."""
    users = load_users()

    users_list = []
    for email, user_data in users.items():
        users_list.append(
            {
                "email": email,
                "name": user_data.get("name", ""),
                "is_pro": user_data.get("is_pro", False),
                "is_admin": user_data.get("is_admin", False),
                "downloads_count": user_data.get("downloads_count", 0),
                "created_at": user_data.get("created_at"),
            }
        )

    return jsonify({"users": users_list, "total": len(users_list)})


@app.route("/api/admin/users/<email>/pro", methods=["POST"])
@admin_required
def toggle_pro(current_user, email):
    """Activar/desactivar PRO para un usuario (solo admin)."""
    users = load_users()

    if email not in users:
        return jsonify({"error": "User not found"}), 404

    # Toggle PRO status
    users[email]["is_pro"] = not users[email].get("is_pro", False)
    save_users(users)

    return jsonify(
        {
            "message": f"PRO status updated for {email}",
            "email": email,
            "is_pro": users[email]["is_pro"],
        }
    )


@app.route("/api/admin/users/<email>", methods=["DELETE"])
@admin_required
def delete_user(current_user, email):
    """Eliminar un usuario (solo admin)."""
    users = load_users()

    if email not in users:
        return jsonify({"error": "User not found"}), 404

    if email == current_user:
        return jsonify({"error": "Cannot delete yourself"}), 400

    del users[email]
    save_users(users)

    return jsonify({"message": f"User {email} deleted successfully"})


# ==================== SISTEMA DE LÍMITES ====================


def check_user_limit(email):
    """
    Verifica si el usuario puede descargar.
    Returns: (can_download: bool, remaining: int, tier: str)
    """
    users = load_users()
    user = users.get(email)

    if not user:
        return False, 0, "UNKNOWN"

    # Verificar si el trial ha expirado
    if user.get("trial_end"):
        trial_end = datetime.fromisoformat(user["trial_end"])
        now = datetime.now()
        
        if now > trial_end:
            # Trial expirado, quitar PRO
            users = load_users()
            users[email]["is_pro"] = False
            users[email]["trial_expired"] = True
            save_users(users)
            user["is_pro"] = False

    # Si es PRO (o en trial), sin límites
    if user.get("is_pro", False):
        # Calcular días restantes del trial
        if user.get("trial_end"):
            trial_end = datetime.fromisoformat(user["trial_end"])
            days_left = (trial_end - datetime.now()).days
            if days_left > 0:
                return True, "∞", f"PRO (Trial: {days_left} días)"
        return True, "∞", "PRO"

    # Contar descargas del mes actual
    usage = load_usage(email)
    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    monthly_downloads = [
        d for d in usage.get("downloads", []) if d.get("month") == current_month
    ]

    used = len(monthly_downloads)
    remaining = FREE_MONTHLY_LIMIT - used

    if remaining > 0:
        return True, remaining, "FREE"
    else:
        return False, 0, "FREE"


def record_user_download(email):
    """Registra una descarga del usuario."""
    usage = load_usage(email)
    now = datetime.now()

    if "downloads" not in usage:
        usage["downloads"] = []

    usage["downloads"].append({"date": now.isoformat(), "month": now.strftime("%Y-%m")})

    save_usage(email, usage)

    # Actualizar contador en usuario
    users = load_users()
    if email in users:
        users[email]["downloads_count"] = users[email].get("downloads_count", 0) + 1
        save_users(users)


@app.route("/api/limits", methods=["GET"])
@token_required
def get_limits(current_user):
    """Obtiene los límites de uso del usuario."""
    can_download, remaining, tier = check_user_limit(current_user)

    return jsonify(
        {
            "tier": tier,
            "can_download": can_download,
            "remaining": remaining if tier == "FREE" else "unlimited",
            "limit": FREE_MONTHLY_LIMIT if tier == "FREE" else "unlimited",
            "message": f"{'Descargas restantes' if tier == 'FREE' else 'Sin límites'}: {remaining if tier == 'FREE' else '∞'}",
        }
    )


# ==================== CLASE DE DESCARGA ====================


class DownloadTask:
    """Clase para manejar tareas de descarga"""

    def __init__(self, task_id, url, name, quality="high", threads=3, user_email=None):
        self.task_id = task_id
        self.url = url
        self.name = name
        self.quality = quality
        self.threads = threads
        self.user_email = user_email
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
                if "Found" in line and "songs" in line:
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

            # Registrar descarga del usuario
            if self.user_email:
                record_user_download(self.user_email)

            # Limpiar temporal
            shutil.rmtree(task_temp_dir)

        except Exception as e:
            self.status = "error"
            self.error = str(e)


# ==================== ENDPOINTS DE DESCARGA ====================


@app.route("/api/health", methods=["GET"])
def health_check():
    """Verificar que el servidor está funcionando"""
    return jsonify({"status": "ok", "message": "Spotify Downloader API is running"})


@app.route("/api/download", methods=["POST"])
@token_required
def start_download(current_user):
    """Iniciar una nueva descarga (requiere autenticación)."""
    data = request.json

    url = data.get("url")
    name = data.get("name", "playlist")
    quality = data.get("quality", "high")
    threads = data.get("threads", 3)

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Verificar límites
    can_download, remaining, tier = check_user_limit(current_user)

    if not can_download:
        return jsonify(
            {
                "error": "Límite alcanzado",
                "message": f"Has usado tu {FREE_MONTHLY_LIMIT} descarga gratuita este mes. Contacta al admin para activar PRO.",
                "tier": tier,
                "upgrade_required": True,
            }
        ), 403

    # Crear tarea de descarga
    task_id = str(uuid.uuid4())
    task = DownloadTask(task_id, url, name, quality, threads, current_user)
    downloads_status[task_id] = task

    # Iniciar descarga
    task.start()

    return jsonify(
        {
            "task_id": task_id,
            "status": "started",
            "message": "Download started successfully",
            "tier": tier,
            "remaining": remaining,
        }
    )


@app.route("/api/status/<task_id>", methods=["GET"])
@token_required
def get_status(current_user, task_id):
    """Obtener estado de una descarga"""
    task = downloads_status.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Verificar que la tarea pertenece al usuario
    if task.user_email != current_user:
        users = load_users()
        if not users.get(current_user, {}).get("is_admin", False):
            return jsonify({"error": "Access denied"}), 403

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
@token_required
def download_file(current_user, task_id):
    """Descargar el archivo ZIP resultante"""
    task = downloads_status.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Verificar que la tarea pertenece al usuario
    if task.user_email != current_user:
        users = load_users()
        if not users.get(current_user, {}).get("is_admin", False):
            return jsonify({"error": "Access denied"}), 403

    if task.status != "completed":
        return jsonify({"error": "Download not completed yet"}), 400

    if not task.zip_path or not os.path.exists(task.zip_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(
        task.zip_path, as_attachment=True, download_name=os.path.basename(task.zip_path)
    )


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🎵 SPOTIFY DOWNLOADER PRO - API CON AUTENTICACIÓN")
    print("=" * 60)
    print("🚀 Server: http://localhost:5001")
    print("📡 API Health: http://localhost:5001/api/health")
    print("=" * 60)
    print("\n👤 ADMIN CREDENTIALS (Por defecto):")
    print("   Email: admin@spotube.com")
    print("   Password: admin123")
    print("=" * 60)
    print("\n🔐 ENDPOINTS:")
    print("   POST /api/auth/register - Registrar usuario")
    print("   POST /api/auth/login - Login")
    print("   GET  /api/auth/me - Info del usuario actual")
    print("   GET  /api/limits - Ver límites de descarga")
    print("   POST /api/download - Iniciar descarga")
    print("")
    print("   👑 ADMIN ONLY:")
    print("   GET    /api/admin/users - Listar usuarios")
    print("   POST   /api/admin/users/<email>/pro - Toggle PRO")
    print("   DELETE /api/admin/users/<email> - Eliminar usuario")
    print("=" * 60 + "\n")

    app.run(debug=True, host="0.0.0.0", port=5001)
