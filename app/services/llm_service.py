import os
import httpx
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

class LLMService:
    def __init__(self):
        # Leer variables de entorno con valores por defecto seguros
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.api_url = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
        self.model = os.getenv("LLM_MODEL", "mistralai/mistral-7b-instruct:free")
        
        # Cabeceras obligatorias requeridas por OpenRouter
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost:8000",  # Requerido por OpenRouter para el ranking de apps
            "X-Title": "Generador de Recetas Inteligente"
        }

    async def _test_connection(self) -> bool:
        """
        Método utilitario interno para comprobar que la API key esté configurada.
        """
        if not self.api_key or self.api_key.startswith("sk-or-..."):
            return False
        return True

# Instancia única del servicio para ser reutilizada (patrón Singleton)
llm_service = LLMService()