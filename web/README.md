# 🌐 Web App - Spotify Downloader PRO

Aplicación web profesional para descargar playlists de Spotify.

## 🚀 Características

- ✨ Interfaz moderna y responsive
- ⚡ Descarga en tiempo real con progreso
- 🎨 Diseño tipo Spotify
- 📱 Funciona en móvil, tablet y desktop
- 🔄 Sistema de backend API REST

## 💻 Cómo Usar

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Iniciar el Backend

```bash
python api.py
```

El servidor iniciará en `http://localhost:5000`

### 3. Abrir la Aplicación Web

Abre `web/index.html` en tu navegador o usa un servidor web local:

```bash
# Opción 1: Usando Python
cd web
python -m http.server 8000

# Opción 2: Usando Live Server (VS Code)
# Click derecho en index.html -> Open with Live Server
```

Luego abre: `http://localhost:8000`

## 📁 Estructura

```
web/
├── index.html      # Página principal
├── styles.css      # Estilos profesionales
└── app.js          # Lógica de la aplicación

api.py              # Backend Flask API
```

## 🎯 Endpoints API

### GET /api/health
Verificar estado del servidor

### POST /api/download
Iniciar una descarga
```json
{
  "url": "https://open.spotify.com/playlist/...",
  "name": "Mi_Musica",
  "quality": "high",
  "threads": 3
}
```

### GET /api/status/<task_id>
Verificar progreso de descarga

### GET /api/download/<task_id>
Descargar archivo ZIP resultante

## 🎨 Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Animaciones**: Particles.js
- **API**: RESTful API
- **Diseño**: Responsive, Mobile-First

## ⚙️ Configuración

Para cambiar el puerto del backend, edita `api.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Para cambiar la URL de la API en el frontend, edita `app.js`:
```javascript
const API_URL = 'http://localhost:5000/api';
```

## 🐛 Solución de Problemas

### Error CORS
Asegúrate de que Flask-CORS está instalado:
```bash
pip install flask-cors
```

### Puerto en uso
Cambia el puerto en `api.py` o cierra el proceso que usa el puerto 5000

### Servidor no disponible
Verifica que el backend esté corriendo:
```bash
curl http://localhost:5000/api/health
```

## 📝 Notas

- El backend debe estar corriendo para que funcione la web app
- Los archivos descargados se guardan en `/downloads`
- Los archivos temporales se crean en `/temp_downloads`

---

Made with ❤️ by Alvaro Manzo
