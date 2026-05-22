# agent/providers/__init__.py — Factory de proveedores
# Generado por AgentKit

"""
Selecciona el proveedor de WhatsApp según la variable WHATSAPP_PROVIDER en .env.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from agent.providers.base import ProveedorWhatsApp

logger = logging.getLogger("agentkit")

# Cargar .env si existe (desarrollo local). En Railway las vars vienen del OS.
_env_path = Path(__file__).parent.parent.parent / ".env"
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path, encoding="utf-8", override=True)


def obtener_proveedor() -> ProveedorWhatsApp:
    """Retorna el proveedor de WhatsApp configurado en WHATSAPP_PROVIDER."""
    proveedor = (os.getenv("WHATSAPP_PROVIDER") or "").strip().lower()

    if not proveedor:
        # Mostrar todas las vars disponibles para diagnóstico
        vars_disponibles = [k for k in os.environ.keys() if not k.startswith("_")]
        logger.error(f"WHATSAPP_PROVIDER no encontrado. Variables disponibles: {vars_disponibles[:20]}")
        raise ValueError(
            "WHATSAPP_PROVIDER no configurado. "
            "En Railway: Ve a tu proyecto -> Variables -> agrega WHATSAPP_PROVIDER=twilio"
        )

    if proveedor == "meta":
        from agent.providers.meta import ProveedorMeta
        return ProveedorMeta()
    elif proveedor == "twilio":
        from agent.providers.twilio import ProveedorTwilio
        return ProveedorTwilio()
    else:
        raise ValueError(f"Proveedor '{proveedor}' no soportado. Usa: meta o twilio")
