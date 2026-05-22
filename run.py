"""Script de arranque — lee PORT del entorno y lanza uvicorn."""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("agent.main:app", host="0.0.0.0", port=port, reload=False)
