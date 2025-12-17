#!/bin/bash

# 🛑 Spotify Downloader PRO - Stop Script

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}⏹️  Deteniendo Spotify Downloader Web...${NC}"

# Buscar y matar procesos de API
API_PID=$(lsof -ti:5001)
if [ ! -z "$API_PID" ]; then
    kill $API_PID 2>/dev/null
    echo -e "${GREEN}✅ API (puerto 5001) detenida${NC}"
else
    echo -e "${YELLOW}⚠️  No se encontró API corriendo en puerto 5001${NC}"
fi

# Buscar y matar procesos del servidor web
WEB_PID=$(lsof -ti:8000)
if [ ! -z "$WEB_PID" ]; then
    kill $WEB_PID 2>/dev/null
    echo -e "${GREEN}✅ Servidor Web (puerto 8000) detenido${NC}"
else
    echo -e "${YELLOW}⚠️  No se encontró servidor web corriendo en puerto 8000${NC}"
fi

echo -e "${GREEN}✅ Todos los servidores detenidos${NC}"
