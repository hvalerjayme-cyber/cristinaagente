# agent/tools.py — Herramientas del agente para Limpia Todo Perú
# Generado por AgentKit

"""
Herramientas específicas del negocio.
Caso de uso: Calificar y atender leads / ventas de servicios de limpieza.
"""

import os
import yaml
import logging
from datetime import datetime

logger = logging.getLogger("agentkit")


def cargar_info_negocio() -> dict:
    """Carga la información del negocio desde business.yaml."""
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}


def obtener_horario() -> dict:
    """Retorna el horario de atención del negocio y si está abierto ahora."""
    info = cargar_info_negocio()
    ahora = datetime.now()
    # Lunes=0 ... Sábado=5 ... Domingo=6
    dia_semana = ahora.weekday()
    hora_actual = ahora.hour

    # Horario: Lunes a Sábado de 8am a 8pm
    esta_abierto = (dia_semana <= 5) and (8 <= hora_actual < 20)

    return {
        "horario": info.get("negocio", {}).get("horario", "Lunes a Sábado de 8am a 8pm"),
        "esta_abierto": esta_abierto,
        "dia_actual": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][dia_semana],
    }


def obtener_precio_servicio(tipo_servicio: str, metros_cuadrados: int) -> dict:
    """
    Calcula el precio estimado según el tipo de servicio y metros cuadrados.

    Args:
        tipo_servicio: 'mantenimiento' o 'profunda'
        metros_cuadrados: Tamaño del hogar en m²

    Returns:
        Diccionario con precio, operarios y horas
    """
    precios = {
        "mantenimiento": [
            {"hasta": 90,  "precio": 199, "operarios": 2, "horas": 4},
            {"hasta": 120, "precio": 250, "operarios": 2, "horas": 5},
            {"hasta": 150, "precio": 299, "operarios": 3, "horas": 4},
            {"hasta": 180, "precio": 375, "operarios": 3, "horas": 5},
            {"hasta": 210, "precio": 450, "operarios": 3, "horas": 6},
        ],
        "profunda": [
            {"hasta": 90,  "precio": 299, "operarios": 2, "horas": 6},
            {"hasta": 120, "precio": 350, "operarios": 2, "horas": 7},
            {"hasta": 150, "precio": 399, "operarios": 3, "horas": 6},
            {"hasta": 180, "precio": 499, "operarios": 3, "horas": 7},
            {"hasta": 210, "precio": 599, "operarios": 4, "horas": 6},
        ],
    }

    tipo = tipo_servicio.lower()
    if tipo not in precios:
        return {"error": f"Tipo de servicio '{tipo_servicio}' no reconocido"}

    for rango in precios[tipo]:
        if metros_cuadrados <= rango["hasta"]:
            return {
                "servicio": tipo_servicio,
                "metros": metros_cuadrados,
                "precio": rango["precio"],
                "operarios": rango["operarios"],
                "horas": rango["horas"],
            }

    return {"error": "Hogar mayor a 210 m², consultar precio especial"}


def registrar_lead(telefono: str, nombre: str, servicio_interes: str, metros: str = "") -> dict:
    """
    Registra un lead interesado para seguimiento.

    Args:
        telefono: Número del cliente
        nombre: Nombre del cliente
        servicio_interes: Servicio en el que está interesado
        metros: Metros cuadrados aproximados (opcional)

    Returns:
        Confirmación del registro
    """
    logger.info(f"LEAD REGISTRADO — Tel: {telefono} | Nombre: {nombre} | Servicio: {servicio_interes} | m²: {metros}")
    # TODO: Integrar con CRM (Alegra, HubSpot, etc.)
    return {
        "registrado": True,
        "mensaje": f"Lead de {nombre} registrado para servicio de {servicio_interes}",
    }


def buscar_en_knowledge(consulta: str) -> str:
    """
    Busca información relevante en los archivos de /knowledge.
    Retorna el contenido más relevante encontrado.
    """
    resultados = []
    knowledge_dir = "knowledge"

    if not os.path.exists(knowledge_dir):
        return "No hay archivos de conocimiento disponibles."

    for archivo in os.listdir(knowledge_dir):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                if consulta.lower() in contenido.lower():
                    resultados.append(f"[{archivo}]: {contenido[:500]}")
        except (UnicodeDecodeError, IOError):
            continue

    if resultados:
        return "\n---\n".join(resultados)
    return "No encontré información específica sobre eso en mis archivos."
