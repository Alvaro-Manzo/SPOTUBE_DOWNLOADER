# 🎵 Spotify Playlist Downloader

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=flat&logo=spotify&logoColor=white)

**Descarga tus playlists de Spotify como archivos MP3 comprimidos en ZIP** 📦

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Contribuir](#-contribuir)

</div>

---

## 📖 Descripción

¿Cansado de descargar canciones una por una? Este script automatiza el proceso de descargar playlists completas de Spotify y las comprime en un archivo ZIP listo para transferir a USB, teléfono o cualquier dispositivo.

## ✨ Características

- 🎧 **Descarga playlists completas** de Spotify automáticamente
- 📦 **Compresión automática** en archivos ZIP
- 🔄 **Manejo inteligente de errores** - continúa descargando aunque algunas canciones fallen
- ⏳ **Control de rate limits** - espera automáticamente cuando YouTube limita las descargas
- 📊 **Reporte detallado** - muestra cuántas canciones se descargaron exitosamente
- 🎯 **Nombres personalizados** para tus archivos ZIP
- 💾 **Listo para USB** - arrastra y suelta en tu dispositivo

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clona el repositorio**
```bash
git clone https://github.com/Alvaro-Manzo/SPOTUBE_DOWNLOADER.git
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
- **Tiempo de descarga**: Depende del tamaño de tu playlist (puede tomar varios minutos u horas :( ).
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
