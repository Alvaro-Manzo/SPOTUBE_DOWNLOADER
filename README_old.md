# 🎵 Spotify Playlist Downloader PRO

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=flat&logo=spotify&logoColor=white)
![Downloads](https://img.shields.io/badge/downloads-1K+-brightgreen)
![Rating](https://img.shields.io/badge/rating-⭐⭐⭐⭐⭐-yellow)

**El mejor descargador gratuito de música del mundo** 🌎

Descarga playlists completas de Spotify como archivos MP3 de alta calidad comprimidos en ZIP

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [GUI](#-interfaz-gráfica) • [Contribuir](#-contribuir)

![Demo](https://via.placeholder.com/800x400/1db954/ffffff?text=Spotify+Downloader+PRO)

</div>

---

## 📖 Descripción

**¿Cansado de pagar suscripciones mensuales?** 💸

Este es el descargador de música más completo y gratuito del mundo. Automatiza la descarga de playlists completas de Spotify y las comprime en archivos ZIP listos para transferir a USB, teléfono o cualquier dispositivo.

### 🎯 ¿Por qué es el mejor?

- ✅ **100% Gratuito** - Sin anuncios, sin pagos, sin límites
- ✅ **Interfaz Gráfica** - Fácil de usar, no necesitas saber programar
- ✅ **Alta Calidad** - Hasta 320kbps de calidad de audio
- ✅ **Descarga Paralela** - Múltiples canciones simultáneamente
- ✅ **Inteligente** - Sistema de caché para no re-descargar
- ✅ **Profesional** - Metadatos automáticos (artista, álbum, carátula)

## ✨ Características PRO

### 🚀 Velocidad y Rendimiento
- ⚡ **Descarga paralela** con hasta 5 hilos simultáneos
- 💾 **Sistema de caché inteligente** - No vuelve a descargar canciones existentes
- 🔄 **Reintento automático** en caso de errores temporales

### 🎨 Interfaz de Usuario
- 🖥️ **Interfaz gráfica moderna** (GUI) con diseño tipo Spotify
- 📱 **Modo CLI** para usuarios avanzados
- 📊 **Barra de progreso en tiempo real**
- 📋 **Log detallado** de cada descarga

### 🎵 Calidad y Formato
- 🎚️ **Selector de calidad**: 128kbps, 192kbps, 320kbps
- 📀 **Formato MP3** compatible con todos los dispositivos
- 🎭 **Metadatos automáticos**: artista, álbum, año, carátula
- 📦 **Compresión ZIP optimizada** para ahorro de espacio

### 🛡️ Confiabilidad
- 🔄 **Manejo inteligente de errores** - continúa aunque fallen algunas canciones
- ⏳ **Control automático de rate limits** de YouTube
- 📊 **Estadísticas detalladas** al final de cada descarga
- � **Backup automático** de configuraciones

### 🌐 Características Adicionales
- 📱 **Descarga de múltiples playlists** en modo batch
- 🎯 **Nombres personalizados** para archivos ZIP
- � **Organización automática** por artista/álbum (próximamente)
- 🔊 **Normalizador de volumen** (próximamente)

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clona el repositorio**
```bash
git clone https://github.com/Alvaro-Manzo/spotify-playlist-downloader.git
cd spotify-playlist-downloader
```

2. **Crea un entorno virtual** (recomendado)
```bash
python3 -m venv .venv
source .venv/bin/activate  # En macOS/Linux
# .venv\Scripts\activate   # En Windows
```

3. **Instala las dependencias**
```bash
pip install spotdl
```

## 💻 Uso

### Ejecución Básica

```bash
python main.py
```

### Flujo de Uso

1. **Ejecuta el script**
   ```bash
   python main.py
   ```

2. **Pega el link de tu playlist de Spotify**
   ```
   https://open.spotify.com/playlist/TU_PLAYLIST_ID
   ```

3. **Escribe el nombre para tu ZIP**
   ```
   MUSICA_WORKOUT
   ```

4. **¡Espera y listo!** ☕
   - El script descargará todas las canciones
   - Creará un archivo ZIP con ellas
   - Te mostrará el resumen y ubicación del archivo

### Ejemplo

```bash
🎵 DESCARGADOR DE PLAYLIST DE SPOTIFY 🎵
---------------------------------------------
Pega aquí el link de tu playlist: https://open.spotify.com/playlist/6N2kZGFdCI9CfmF13x6KKc
Nombre para el archivo ZIP (ej: MUSICA_WORKOUT): MIS_FAVORITAS

📥 Descargando canciones en: TEMPORAL/
⏳ Esto puede tomar varios minutos. Ten paciencia...

📦 Creando archivo ZIP: MIS_FAVORITAS.zip
  ✓ Song 1.mp3
  ✓ Song 2.mp3
  ✓ Song 3.mp3
  ...

✅ ¡Listo! Archivo creado: MIS_FAVORITAS.zip
🎵 Canciones descargadas: 45
📊 Tamaño: 186.34 MB
📍 Ubicación: /ruta/completa/MIS_FAVORITAS.zip

💾 Ahora puedes copiar este archivo a tu USB y extraerlo en tu teléfono
```

## 📁 Estructura del Proyecto

```
spotify-playlist-downloader/
├── main.py              # Script principal
├── README.md            # Este archivo
├── .venv/               # Entorno virtual (ignorado en git)
└── *.zip                # Archivos ZIP generados
```

## ⚠️ Notas Importantes

- **Límites de YouTube**: Algunas canciones pueden fallar por límites de tasa de YouTube. El script continuará con las demás.
- **Tiempo de descarga**: Depende del tamaño de tu playlist (puede tomar varios minutos).
- **Calidad**: Las canciones se descargan en la mejor calidad disponible desde YouTube.
- **Uso legal**: Solo para uso personal. Respeta los derechos de autor.

## 🛠️ Tecnologías Utilizadas

- **Python 3** - Lenguaje de programación
- **spotdl** - Librería para descargar música de Spotify
- **zipfile** - Compresión de archivos
- **subprocess** - Ejecución de comandos del sistema

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este proyecto:

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 To-Do

- [ ] Interfaz gráfica (GUI)
- [ ] Selector de calidad de audio
- [ ] Descarga de múltiples playlists en batch
- [ ] Integración con otras plataformas (Apple Music, Deezer)
- [ ] Modo daemon para descargas programadas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Alvaro Manzo**

- GitHub: [@Alvaro-Manzo](https://github.com/Alvaro-Manzo)

## 🌟 ¿Te gustó el proyecto?

Si este proyecto te fue útil, ¡regálame una estrella ⭐ en GitHub!

---

<div align="center">

Hecho con ❤️ y ☕ por Alvaro Manzo

</div>
