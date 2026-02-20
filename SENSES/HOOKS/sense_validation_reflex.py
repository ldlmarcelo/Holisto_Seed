import json
import sys
import os

# Palabras que indican una intención o explicación
INTENT_SIGNALS = ["porque", "para", "objetivo", "razón", "error", "fallo", "necesito", "quiero", "resolver", "fix"]

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"status": "proceed"}))
            return

        payload = json.loads(input_data)
        # El hook BeforeAgent recibe el prompt del usuario en 'prompt'
        user_prompt = payload.get("prompt", "").strip().lower()
        
        if not user_prompt:
            print(json.dumps({"status": "proceed"}))
            return

        # 1. Análisis de Intención (PIP - Protocolo de Intención Profunda)
        # Un prompt es sospechoso de Problema XY si es corto y no tiene señales de intención.
        words = user_prompt.split()
        is_short = len(words) < 7
        has_intent = any(signal in user_prompt for signal in INTENT_SIGNALS)
        
        output = {"status": "proceed"}
        
        if is_short and not has_intent:
            msg = "ALERTA PIP: Instrucción técnica detectada sin contexto de intención. Riesgo de Problema XY."
            output["systemMessage"] = f"[\033[94m? DEEP INTENT\033[0m] {msg}"
            output["hookSpecificOutput"] = {
                "additionalContext": "¡ATENCIÓN! El prompt del usuario es una instrucción técnica directa y breve. Antes de ejecutar, DEBES aplicar el PIP: Pregunta socráticamente por el objetivo raíz ('¿Qué problema estamos intentando resolver con esto?') para evitar la deriva técnica."
            }
            print(json.dumps(output))
            return

        # 2. Análisis de Sentido (PVS - Validación de Sentido)
        # (Aquí se podría añadir lógica para comparar con el Roadmap, 
        # pero por ahora nos enfocamos en el PIP que es el más urgente).
        
        print(json.dumps(output))

    except Exception as e:
        sys.stderr.write(f"Error en sense-validation hook: {str(e)}
")
        print(json.dumps({"status": "error_but_proceed", "error": str(e)}))

if __name__ == "__main__":
    main()
