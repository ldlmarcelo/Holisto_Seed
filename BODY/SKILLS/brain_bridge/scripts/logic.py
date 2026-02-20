import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# --- Universal Root Discovery ---
try:
    from BODY.UTILS.terroir_locator import TerroirLocator
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
    from BODY.UTILS.terroir_locator import TerroirLocator

class BrainBridge:
    """
    Capa de abstraccion para conectividad con LLMs.
    Implementa el patron de diseño 'Model Router'.
    """
    
    def __init__(self, settings_path=None):
        self.seed_root = TerroirLocator.get_seed_root()
        self.settings_path = Path(settings_path) if settings_path else self.seed_root / "CORE" / "settings.json"
        self.settings = self._load_settings()
        load_dotenv(TerroirLocator.get_orchestrator_root() / ".env")
        
        self.logger = logging.getLogger("brain_bridge")
        self._setup_provider()

    def _load_settings(self) -> dict:
        if not self.settings_path.exists():
            return {"model_routing": {"default_brain": "gemini-2.0-flash"}}
        with open(self.settings_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _setup_provider(self):
        self.default_brain = self.settings.get("model_routing", {}).get("default_brain", "gemini-2.0-flash")
        
        # Detectar el proveedor basado en el nombre del modelo
        if "gemini" in self.default_brain:
            self.provider_type = "google"
            self._init_google()
        elif "ollama" in self.default_brain:
            self.provider_type = "ollama"
            self._init_ollama()
        else:
            self.provider_type = "unknown"

    def _init_google(self):
        try:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.model_instance = genai.GenerativeModel(self.default_brain)
            else:
                self.model_instance = None
        except ImportError:
            self.model_instance = None

    def _init_ollama(self):
        # Placeholder para futura integracion con Ollama
        self.model_instance = None

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        """Metodo universal para generar respuestas."""
        if self.provider_type == "google" and self.model_instance:
            try:
                # Si se requiere instruccion de sistema, creamos un nuevo modelo con ella
                if system_instruction:
                    import google.generativeai as genai
                    temp_model = genai.GenerativeModel(self.default_brain, system_instruction=system_instruction)
                    response = temp_model.generate_content(prompt)
                else:
                    response = self.model_instance.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Error en BrainBridge (Google): {str(e)}"
        
        return f"Error: Proveedor '{self.provider_type}' no inicializado correctamente para el modelo '{self.default_brain}'."

if __name__ == "__main__":
    # Prueba rapida
    bridge = BrainBridge()
    print(f"BrainBridge activo usando: {bridge.default_brain}")
    # res = bridge.generate("Hola Holisto, ¿quién eres?")
    # print(res)
