---
name: brain-bridge
description: Interfaz universal de comunicación con modelos de lenguaje (LLMs).
---

# Skill: Brain Bridge

## 🛠️ Lógica de Ejecución
Este órgano actúa como una capa de abstracción sobre los proveedores de IA. Lee la configuración de `CORE/settings.json` y enruta las peticiones de texto al cerebro correspondiente (Gemini, OpenAI, Ollama, etc.), asegurando que el resto de las Skills no dependan de una API específica.

## 🚀 Uso Programático
```python
from BODY.SKILLS.brain_bridge.scripts.logic import BrainBridge
bridge = BrainBridge()
response = bridge.generate("Hola The Individual")
```
