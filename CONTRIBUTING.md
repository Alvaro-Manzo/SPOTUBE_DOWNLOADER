# 🤝 Contribuir a Spotube Downloader

¡Gracias por tu interés en contribuir! Este proyecto busca ser el mejor descargador gratuito de música, y tu ayuda es bienvenida.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Contribuir?](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Guía de Desarrollo](#guía-de-desarrollo)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)

## 📜 Código de Conducta

Este proyecto sigue un código de conducta para asegurar un ambiente acogedor:

- **Sé respetuoso**: Trata a todos con respeto y consideración
- **Sé constructivo**: Las críticas deben ser constructivas y útiles
- **Sé colaborativo**: Trabajamos juntos para mejorar el proyecto
- **Sé paciente**: Todos estamos aprendiendo

## 🚀 ¿Cómo Contribuir?

Hay muchas formas de contribuir:

1. **Reportar bugs** 🐛
2. **Sugerir nuevas funcionalidades** 💡
3. **Mejorar documentación** 📝
4. **Escribir código** 💻
5. **Revisar Pull Requests** 👀
6. **Traducir la interfaz** 🌍

## 🛠️ Configuración del Entorno

### Prerrequisitos

- Python 3.8+
- Git
- FFmpeg
- Make (opcional pero recomendado)

### Instalación

1. **Fork el repositorio**
   ```bash
   # Haz clic en "Fork" en GitHub
   ```

2. **Clona tu fork**
   ```bash
   git clone https://github.com/TU-USUARIO/SPOTUBE_DOWNLOADER.git
   cd SPOTUBE_DOWNLOADER
   ```

3. **Configura el repositorio upstream**
   ```bash
   git remote add upstream https://github.com/Alvaro-Manzo/SPOTUBE_DOWNLOADER.git
   ```

4. **Crea un entorno virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

5. **Instala dependencias de desarrollo**
   ```bash
   make install  # O: pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

6. **Instala pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 💻 Guía de Desarrollo

### Estructura del Proyecto

```
SPOTUBE_DOWNLOADER/
├── main.py          # CLI básico
├── main_pro.py      # CLI avanzado
├── gui.py           # Interfaz gráfica
├── api.py           # Backend API
├── web/             # Frontend web
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/           # Tests automatizados
├── Dockerfile       # Imagen Docker
└── docker-compose.yml
```

### Workflow de Desarrollo

1. **Crea una rama para tu feature**
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```

2. **Haz tus cambios**
   ```bash
   # Edita archivos
   ```

3. **Ejecuta tests**
   ```bash
   make test  # O: pytest
   ```

4. **Formatea el código**
   ```bash
   make format  # O: black .
   ```

5. **Verifica el linting**
   ```bash
   make lint  # O: flake8
   ```

6. **Commit tus cambios**
   ```bash
   git add .
   git commit -m "✨ feat: descripción clara del cambio"
   ```

### Convenciones de Código

#### Python

- **PEP 8**: Sigue las guías de estilo de Python
- **Black**: Formateador automático (línea máx: 100 caracteres)
- **Type Hints**: Usa anotaciones de tipo cuando sea posible
- **Docstrings**: Documenta funciones y clases

```python
def descargar_playlist(url: str, calidad: str = "320k") -> bool:
    """
    Descarga una playlist de Spotify.
    
    Args:
        url: URL de la playlist de Spotify
        calidad: Calidad del audio (128k, 192k, 320k)
        
    Returns:
        True si la descarga fue exitosa, False en caso contrario
        
    Raises:
        ValueError: Si la URL no es válida
    """
    pass
```

#### JavaScript

- **ESLint**: Sigue las reglas configuradas
- **Prettier**: Formateador automático
- **Camel Case**: Para variables y funciones
- **Comentarios**: Documenta lógica compleja

```javascript
/**
 * Inicia la descarga de una playlist
 * @param {string} playlistUrl - URL de la playlist
 * @returns {Promise<Object>} - Respuesta del servidor
 */
async function startDownload(playlistUrl) {
  // ...
}
```

### Commits Semánticos

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `✨ feat:` Nueva funcionalidad
- `🐛 fix:` Corrección de bug
- `📝 docs:` Cambios en documentación
- `💄 style:` Cambios de formato (no afectan lógica)
- `♻️ refactor:` Refactorización de código
- `⚡ perf:` Mejoras de rendimiento
- `✅ test:` Añadir o actualizar tests
- `🏗️ build:` Cambios en build o dependencias
- `🔧 chore:` Tareas de mantenimiento

**Ejemplos:**
```bash
git commit -m "✨ feat: añadir soporte para playlists privadas"
git commit -m "🐛 fix: corregir error en descarga de álbumes"
git commit -m "📝 docs: actualizar README con ejemplos de Docker"
```

## 🔄 Proceso de Pull Request

1. **Asegúrate de que tu código pasa todos los tests**
   ```bash
   make check  # Ejecuta tests, lint y formato
   ```

2. **Actualiza la documentación** si es necesario

3. **Actualiza el CHANGELOG.md** con tus cambios

4. **Push a tu fork**
   ```bash
   git push origin feature/nombre-descriptivo
   ```

5. **Abre un Pull Request** en GitHub
   - Título descriptivo
   - Descripción detallada de los cambios
   - Referencias a issues relacionados
   - Screenshots si hay cambios visuales

6. **Responde a los comentarios** de los revisores

7. **Espera la aprobación** y merge

### Checklist del PR

```markdown
- [ ] Tests pasan localmente
- [ ] Código formateado con Black
- [ ] Sin errores de Flake8
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado
- [ ] Commits siguen convención semántica
- [ ] PR vinculado a issue relevante
```

## 🐛 Reportar Bugs

Usa la plantilla de issues de GitHub:

**Título**: Breve descripción del bug

**Descripción**:
- Qué esperabas que pasara
- Qué pasó en realidad
- Pasos para reproducir
- Capturas de pantalla (si aplica)

**Entorno**:
- OS: macOS/Windows/Linux
- Python: 3.x.x
- Versión de spotube-downloader: x.x.x

**Logs**:
```
Pega aquí los logs relevantes
```

## 💡 Sugerir Mejoras

Usa la plantilla de feature request:

**Título**: Breve descripción de la mejora

**Problema**: ¿Qué problema resuelve?

**Solución propuesta**: ¿Cómo lo resolverías?

**Alternativas**: Otras soluciones consideradas

**Contexto adicional**: Mockups, ejemplos, etc.

## 🧪 Tests

### Escribir Tests

```python
# tests/test_feature.py
import pytest

def test_descargar_playlist_valida():
    """Test que verifica descarga de playlist válida."""
    url = "https://open.spotify.com/playlist/..."
    resultado = descargar_playlist(url)
    assert resultado is True

def test_url_invalida_lanza_error():
    """Test que verifica manejo de URL inválida."""
    with pytest.raises(ValueError):
        descargar_playlist("url-invalida")
```

### Ejecutar Tests

```bash
# Todos los tests
make test

# Con coverage
make coverage

# Tests específicos
pytest tests/test_api.py

# En modo watch
pytest-watch
```

## 📦 Releases

Los maintainers crean releases siguiendo [Semantic Versioning](https://semver.org/):

- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Nueva funcionalidad compatible
- **PATCH**: Correcciones de bugs

## 🙏 Reconocimientos

Todos los contribuidores son reconocidos en:
- README.md (sección Contributors)
- GitHub Contributors page
- CHANGELOG.md para cada release

## 📞 Contacto

- **Issues**: Para bugs y features
- **Discussions**: Para preguntas y discusiones generales
- **Discord**: [Enlace al servidor] (si existe)

---

**¡Gracias por contribuir a hacer este el mejor descargador de música gratuito del mundo! 🎵🚀**
