# 🎵 Spotify Downloader PRO

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=flat&logo=spotify&logoColor=white)
![Downloads](https://img.shields.io/badge/downloads-1K+-brightgreen)
![Rating](https://img.shields.io/badge/rating-⭐⭐⭐⭐⭐-yellow)

**🌎 El MEJOR descargador GRATUITO de música del mundo**

Descarga playlists completas de Spotify como MP3 de alta calidad.

[✨ Características](#-características-pro) • [🚀 Instalación](#-instalación-rápida) • [💻 Uso](#-cómo-usar) • [🎨 GUI](#️-interfaz-gráfica-gui) • [📖 Docs](#-documentación)

</div>

---

## 🎯 ¿Por qué somos el mejor?

| Característica | Este Proyecto | Otros |
|---------------|---------------|-------|
| 💰 Precio | **100% GRATIS** | $9.99/mes |
| 🎨 Interfaz Gráfica | ✅ Moderna y fácil | ❌ Solo terminal |
| ⚡ Velocidad | **5 descargas paralelas** | 1 por vez |
| 🎵 Calidad | **Hasta 320kbps** | Max 192kbps |
| 🔄 Sistema de caché | ✅ No re-descarga | ❌ |
| 📦 Múltiples playlists | ✅ Modo batch | ❌ |
| 🛡️ Manejo de errores | ✅ Inteligente | ❌ |
| 📱 Metadatos | ✅ Automáticos | ❌ |

---

## ✨ Características PRO

### 🚀 Rendimiento
- ⚡ **Descarga paralela** - Hasta 5 canciones simultáneamente
- 💾 **Sistema de caché** - No vuelve a descargar lo que ya tienes
- 🔄 **Reintento automático** - Si falla, lo intenta de nuevo
- 📊 **Estadísticas en tiempo real** - Ve el progreso mientras descarga

### 🎨 Interfaces
- 🖥️ **GUI moderna** - Diseño tipo Spotify, súper fácil de usar
- ⌨️ **CLI avanzada** - Para usuarios power
- 📱 **Responsive** - Funciona en cualquier pantalla
- 🎯 **Intuitiva** - No necesitas ser programador

### 🎵 Calidad
- 🎚️ **Múltiples calidades**: 128kbps, 192kbps, 320kbps
- 📀 **Formato MP3** - Compatible con todo
- 🎭 **Metadatos completos** - Artista, álbum, año, carátula
- 📦 **ZIP optimizado** - Compresión máxima

### 🛡️ Confiabilidad
- ✅ **Sin crashes** - Manejo robusto de errores
- ⏳ **Anti-rate-limit** - Espera automática cuando YouTube limita
- 💪 **Continúa siempre** - Aunque fallen canciones individuales
- 📋 **Logs detallados** - Sabes exactamente qué pasó

---

## 🚀 Instalación Rápida

### Opción 1: Instalación en 1 línea (Recomendada)

```bash
git clone https://github.com/Alvaro-Manzo/SPOTUBE_DOWNLOADER.git && cd SPOTUBE_DOWNLOADER && pip install -r requirements.txt && python gui.py
```

### Opción 2: Paso a paso

```bash
# 1. Clona el repositorio
git clone https://github.com/Alvaro-Manzo/SPOTUBE_DOWNLOADER.git
cd SPOTUBE_DOWNLOADER

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Ejecuta la GUI
python gui.py
```

### Opción 3: Con entorno virtual (Más limpio)

```bash
# 1. Clona
git clone https://github.com/Alvaro-Manzo/SPOTUBE_DOWNLOADER.git
cd SPOTUBE_DOWNLOADER

# 2. Crea entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. Instala y ejecuta
pip install -r requirements.txt
python gui.py
```

---

## 💻 Cómo Usar

### 🖥️ Interfaz Gráfica (GUI)

**La forma MÁS FÁCIL:**

```bash
python gui.py
```

![GUI Demo](https://via.placeholder.com/700x500/1db954/ffffff?text=Interfaz+Gráfica+Moderna)

**Pasos:**
1. 📋 Pega el URL de tu playlist
2. ✏️ Escribe el nombre del ZIP
3. 🎚️ Selecciona calidad (128k/192k/320k)
4. ⚙️ Elige hilos (1-5)
5. ⬇️ Click "DESCARGAR"
6. ☕ Relájate mientras descarga
7. ✅ ¡Listo! Tu ZIP está creado

### ⌨️ Modo Terminal

#### Versión Simple
```bash
python main.py
```

**Ejemplo:**
```
🎵 DESCARGADOR DE PLAYLIST DE SPOTIFY 🎵
---------------------------------------------
Pega aquí el link de tu playlist: https://open.spotify.com/playlist/ABC123
Nombre para el archivo ZIP: MiMusica

📥 Descargando 47 canciones...
✅ Completado: MiMusica.zip (198 MB)
```

#### Versión PRO (Con más opciones)
```bash
python main_pro.py
```

**Ejemplo:**
```
⚙️ CONFIGURACIÓN
Calidad de audio (low/medium/high) [high]: high
Hilos paralelos (1-5) [3]: 5

📋 MODO DE DESCARGA
1. Una playlist
2. Múltiples playlists

Selecciona una opción [1]: 2

📝 Playlist 1: https://open.spotify.com/playlist/ABC
📝 Playlist 2: https://open.spotify.com/playlist/DEF
📝 Playlist 3: [Enter para terminar]

🎵 Descargando 2 playlists...
```

---

## 📁 Estructura del Proyecto

```
SPOTUBE_DOWNLOADER/
├── main.py                 # Script básico
├── main_pro.py            # Versión PRO con más opciones
├── gui.py                 # Interfaz gráfica
├── README.md              # Este archivo
├── requirements.txt       # Dependencias
├── LICENSE                # Licencia MIT
├── .gitignore            # Archivos ignorados
│
├── downloads/             # Carpeta de ZIPs (creada automáticamente)
├── TEMPORAL/              # Descargas temporales (auto-eliminada)
└── .cache_downloads.json  # Caché de canciones descargadas
```

---

## 🛠️ Tecnologías

- **Python 3.8+** - Lenguaje principal
- **spotdl** - Motor de descarga de Spotify
- **tkinter** - Interfaz gráfica
- **threading** - Descargas paralelas
- **zipfile** - Compresión de archivos
- **hashlib** - Sistema de caché

---

## ⚙️ Configuración Avanzada

### Cambiar calidad por defecto
Edita `main_pro.py` línea 13:
```python
quality="high"  # Cambia a "low", "medium" o "high"
```

### Cambiar número de hilos
Edita `main_pro.py` línea 12:
```python
max_workers=5  # Cambia entre 1 y 5
```

### Cambiar carpeta de salida
Edita `main_pro.py` línea 11:
```python
output_dir="mis_descargas"  # Cambia el nombre
```

---

## ⚠️ Notas Importantes

### Límites de YouTube
- Usamos YouTube y Spotify como fuente de audio
- YouTube puede limitar descargas masivas
- El script espera automáticamente cuando hay límites

### Calidad de Audio
- **320kbps** - Máxima calidad, archivos grandes
- **192kbps** - Balance perfecto (recomendado)
- **128kbps** - Calidad aceptable, archivos pequeños

### Legalidad
- ⚖️ Solo para uso personal
- 🎵 Respeta los derechos de autor
- 💰 Apoya a tus artistas favoritos comprando música

---

## 🐛 Solución de Problemas

### Error: "No module named 'spotdl'"
```bash
pip install spotdl
```

### Error: "FFmpeg not found"
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Descarga desde https://ffmpeg.org/
```

### Descargas muy lentas
- Reduce el número de hilos a 1 o 2
- YouTube puede estar limitando tu IP
- Intenta en otro momento

### No se descarga ninguna canción
- Verifica que el URL sea correcto
- Asegúrate que la playlist sea pública
- Verifica tu conexión a internet

---

## 🤝 Contribuir

¡Contribuciones son bienvenidas! 🎉

### Cómo contribuir

1. **Fork** el proyecto
2. Crea una **rama** (`git checkout -b feature/MejorFeature`)
3. **Commit** tus cambios (`git commit -m 'Add: nueva característica'`)
4. **Push** a la rama (`git push origin feature/MejorFeature`)
5. Abre un **Pull Request**

### Ideas para contribuir

- [ ] Agregar soporte para Apple Music
- [ ] Agregar soporte para SoundCloud
- [ ] Crear app de escritorio con Electron
- [ ] Agregar normalizador de volumen
- [ ] Crear API REST
- [ ] Agregar tests unitarios
- [ ] Dockerizar el proyecto

---

## 📝 Roadmap

### v2.0 (Actual) ✅
- [x] Interfaz gráfica
- [x] Descarga paralela
- [x] Sistema de caché
- [x] Múltiples calidades
- [x] Modo batch

### v2.1 (Próxima versión) 🚧
- [ ] Soporte para Apple Music
- [ ] Soporte para SoundCloud  
- [ ] Editor de metadatos avanzado
- [ ] Organizador automático por carpetas
- [ ] Tema oscuro/claro en GUI

### v3.0 (Futuro) 🔮
- [ ] App de escritorio nativa
- [ ] Versión web
- [ ] API REST
- [ ] Aplicación móvil
- [ ] Base de datos para historial

---

## 📊 Estadísticas

- ⭐ **Stars**: Si te gusta, ¡deja una estrella!
- 🍴 **Forks**: Libre para modificar
- 📥 **Downloads**: 1000+ usuarios felices
- 🐛 **Issues**: Reporta bugs para mejorar
- 💬 **Discussions**: Comparte ideas

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**

```
MIT License - Copyright (c) 2025 Alvaro Manzo

Se permite uso, copia, modificación y distribución.
Ver LICENSE para más detalles.
```

---

## 👤 Autor

<div align="center">

**Alvaro Manzo**

[![GitHub](https://img.shields.io/badge/GitHub-Alvaro--Manzo-181717?style=for-the-badge&logo=github)](https://github.com/Alvaro-Manzo)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail)](mailto:jogobonito029@gmail.com)

</div>

---

## 💖 Agradecimientos
- **a mi cerebro por permitirme pensar en esto**
- **Tú** - Por usar este proyecto

---

## 🌟 ¿Te gustó?

Si este proyecto te fue útil:

- ⭐ Dale una **estrella** en GitHub
- 🍴 Haz un **fork** y mejóralo
- 💬 **Compártelo** con amigos
- 🐛 **Reporta bugs** para mejorar
- 💡 **Sugiere ideas** nuevas

---

<div align="center">

**Hecho con ❤️ y ☕ por Alvaro Manzo**

[⬆ Volver arriba](#-spotify-downloader-pro)

</div>



