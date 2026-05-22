# tests/test_local.py — Simulador de chat en terminal
# Generado por AgentKit — Limpia Todo Perú

"""
Prueba a Cristina sin necesitar WhatsApp.
Simula una conversación en la terminal como si fueras un cliente.
"""

import asyncio
import sys
import os

# Forzar UTF-8 en la terminal de Windows para soportar emojis y tildes
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stdin.encoding != "utf-8":
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.brain import generar_respuesta
from agent.memory import inicializar_db, guardar_mensaje, obtener_historial, limpiar_historial

TELEFONO_TEST = "test-local-001"


async def main():
    """Loop principal del chat de prueba con Cristina."""
    await inicializar_db()

    print()
    print("=" * 60)
    print("   Cristina — Agente de Limpia Todo Perú")
    print("   Test Local (sin WhatsApp)")
    print("=" * 60)
    print()
    print("  Escribe mensajes como si fueras un cliente.")
    print("  Comandos especiales:")
    print("    'limpiar'  — borra el historial de esta sesión")
    print("    'salir'    — termina el test")
    print()
    print("-" * 60)
    print()

    while True:
        try:
            mensaje = input("Cliente: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nTest finalizado. ¡Hasta pronto!")
            break

        if not mensaje:
            continue

        if mensaje.lower() == "salir":
            print("\nTest finalizado. ¡Hasta pronto!")
            break

        if mensaje.lower() == "limpiar":
            await limpiar_historial(TELEFONO_TEST)
            print("[Historial borrado — nueva conversación]\n")
            continue

        # Obtener historial ANTES de guardar el mensaje actual
        historial = await obtener_historial(TELEFONO_TEST)

        # Generar respuesta de Cristina
        print("\nCristina: ", end="", flush=True)
        respuesta = await generar_respuesta(mensaje, historial)
        print(respuesta)
        print()

        # Guardar mensaje del cliente y respuesta de Cristina
        await guardar_mensaje(TELEFONO_TEST, "user", mensaje)
        await guardar_mensaje(TELEFONO_TEST, "assistant", respuesta)


if __name__ == "__main__":
    asyncio.run(main())
