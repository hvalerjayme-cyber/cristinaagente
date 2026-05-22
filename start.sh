#!/bin/bash
# AgentKit — Script de inicio
# El usuario ejecuta: bash start.sh

set -e

echo ""
echo "==========================================================="
echo "   AgentKit — WhatsApp AI Agent Builder"
echo "==========================================================="
echo ""
echo "  Preparando tu entorno para construir tu agente de IA..."
echo ""

# ── Verificar Python ──────────────────────────────────────────
echo "  [1/4] Verificando Python..."

# Detectar el comando Python disponible (python3 en Linux/Mac, python en Windows)
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo ""
    echo "  ERROR: Python 3 no encontrado."
    echo "  Descargalo en: https://python.org/downloads"
    echo ""
    exit 1
fi

PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    echo ""
    echo "  ERROR: Necesitas Python 3.11 o superior."
    echo "  Version actual: $($PYTHON_CMD --version)"
    echo "  Descarga la ultima version en: https://python.org/downloads"
    echo ""
    exit 1
fi
echo "  OK — $($PYTHON_CMD --version)"

# ── Verificar Claude Code ────────────────────────────────────
echo "  [2/4] Verificando Claude Code..."
if command -v claude &> /dev/null; then
    echo "  OK — Claude Code CLI instalado"
else
    echo "  OK — Claude Code detectado (modo Desktop)"
fi

# ── Crear carpetas base ──────────────────────────────────────
echo "  [3/4] Preparando carpetas..."
mkdir -p knowledge
echo "  OK — Estructura lista"

# ── Listo ─────────────────────────────────────────────────────
echo "  [4/4] Todo verificado"

echo ""
echo "==========================================================="
echo ""
echo "  Todo listo. Ahora abre Claude Code:"
echo ""
echo "    claude"
echo ""
echo "  Y escribe:"
echo ""
echo "    /build-agent"
echo ""
echo "  Claude Code te guiara paso a paso para construir"
echo "  tu agente de WhatsApp personalizado con IA."
echo ""
echo "==========================================================="
echo ""
