#!/bin/bash

# 🎵 Spotify Downloader PRO - Web Starter
# Este script inicia tanto el backend API como el frontend web

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════╗"
echo "║  🎵 SPOTIFY DOWNLOADER PRO - WEB APP 🎵  ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar si existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ No se encontró el entorno virtual (.venv)${NC}"
    echo -e "${YELLOW}🔧 Creando entorno virtual...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
    
    echo -e "${YELLOW}📦 Instalando dependencias...${NC}"
    .venv/bin/pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
fi

# Activar entorno virtual
echo -e "${BLUE}🔌 Activando entorno virtual...${NC}"
source .venv/bin/activate

# Verificar que Flask esté instalado
if ! .venv/bin/python -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}📦 Instalando Flask...${NC}"
    .venv/bin/pip install flask flask-cors
fi

echo ""
echo -e "${GREEN}🚀 Iniciando aplicación web...${NC}"
echo ""

# Función para manejar Ctrl+C
cleanup() {
    echo ""
    echo -e "${YELLOW}⏹️  Deteniendo servidores...${NC}"
    kill $API_PID 2>/dev/null
    kill $WEB_PID 2>/dev/null
    echo -e "${GREEN}✅ Servidores detenidos${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar API en background
echo -e "${BLUE}🔧 Iniciando API Backend en puerto 5001...${NC}"
.venv/bin/python api.py > /dev/null 2>&1 &
API_PID=$!

# Esperar a que la API esté lista
sleep 2

# Verificar que la API esté corriendo
if ! ps -p $API_PID > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: No se pudo iniciar el API${NC}"
    exit 1
fi

echo -e "${GREEN}✅ API corriendo en http://localhost:5001${NC}"

# Iniciar servidor web en background
echo -e "${BLUE}🌐 Iniciando Frontend Web en puerto 8000...${NC}"
cd web && ../.venv/bin/python -m http.server 8000 > /dev/null 2>&1 &
WEB_PID=$!
cd ..

# Esperar a que el servidor web esté listo
sleep 1

# Verificar que el servidor web esté corriendo
if ! ps -p $WEB_PID > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: No se pudo iniciar el servidor web${NC}"
    kill $API_PID 2>/dev/null
    exit 1
fi

echo -e "${GREEN}✅ Frontend corriendo en http://localhost:8000${NC}"
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                   ║${NC}"
echo -e "${GREEN}║  ✨ ¡APLICACIÓN WEB LISTA! ✨                     ║${NC}"
echo -e "${GREEN}║                                                   ║${NC}"
echo -e "${GREEN}║  🌐 Abre tu navegador en:                        ║${NC}"
echo -e "${GREEN}║     ${BLUE}http://localhost:8000${GREEN}                       ║${NC}"
echo -e "${GREEN}║                                                   ║${NC}"
echo -e "${GREEN}║  📡 API disponible en:                           ║${NC}"
echo -e "${GREEN}║     ${BLUE}http://localhost:5001${GREEN}                       ║${NC}"
echo -e "${GREEN}║                                                   ║${NC}"
echo -e "${GREEN}║  ⏹️  Presiona Ctrl+C para detener                ║${NC}"
echo -e "${GREEN}║                                                   ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""

# Intentar abrir el navegador automáticamente
if command -v open &> /dev/null; then
    # macOS
    echo -e "${BLUE}🌍 Abriendo navegador...${NC}"
    sleep 1
    open http://localhost:8000
elif command -v xdg-open &> /dev/null; then
    # Linux
    echo -e "${BLUE}🌍 Abriendo navegador...${NC}"
    sleep 1
    xdg-open http://localhost:8000
elif command -v start &> /dev/null; then
    # Windows (Git Bash)
    echo -e "${BLUE}🌍 Abriendo navegador...${NC}"
    sleep 1
    start http://localhost:8000
fi

# Mantener el script corriendo
echo -e "${YELLOW}📊 Logs en tiempo real:${NC}"
echo -e "${YELLOW}   (Los servidores están corriendo en background)${NC}"
echo ""

# Mantener vivo el script
wait $API_PID $WEB_PID
