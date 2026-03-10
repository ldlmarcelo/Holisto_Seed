import json
import sys
import os

# Umbral de turnos silenciosos antes de la alerta
THRESHOLD = 3 

# Palabras clave que indican una respuesta de validación del usuario (resetean el contador)
VALIDATION_KEYWORDS = ["excelente", "bien", "sigue", "perfecto", "adelante", "ok", "listo", "visto", "entendido"]

def main():
    try:
        # El hook recibe el contexto actual por stdin
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"status": "proceed"}))
            return

        payload = json.loads(input_data)
        transcript_path = payload.get("transcript_path")
        
        if not transcript_path or not os.path.exists(transcript_path):
            print(json.dumps({"status": "proceed"}))
            return

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        messages = transcript.get("messages", [])
        
        # 1. Chequeo de PSD (Protocolo de Suspensión Deliberada)
        # Si las últimas interacciones mencionan "Modo Flujo" o "PSD", desactivamos el hook.
        recent_text = " ".join([m.get("content", "").lower() for m in messages[-5:]])
        if "modo flujo" in recent_text or "psd" in recent_text:
            print(json.dumps({"status": "proceed", "message": "PSD activo (Modo Flujo). Reflejo en pausa."}))
            return

        # 2. Conteo de Turnos Silenciosos
        # Un turno es silencioso si el agente hizo trabajo técnico y el usuario solo dijo "adelante" o similar.
        silent_turns = 0
        
        # Iteramos sobre los mensajes del final hacia atrás
        # Buscamos pares (User -> Gemini)
        i = len(messages) - 1
        while i >= 0:
            msg = messages[i]
            
            # Buscamos el mensaje del usuario que disparó el turno
            if msg.get("type") == "user":
                user_content = msg.get("content", "").strip().lower()
                
                # Si el usuario dio feedback real (más de 3 palabras y no es una keyword simple)
                if len(user_content.split()) > 3 and not any(kw == user_content for kw in VALIDATION_KEYWORDS):
                    break # Se rompe la racha de silencio
                
                # Si llegamos aquí, el mensaje del usuario fue corto/silencioso. 
                # Ahora vemos si el agente hizo trabajo técnico en el turno anterior.
                if i > 0 and messages[i-1].get("type") == "gemini":
                    agent_msg = messages[i-1]
                    # Si el agente usó herramientas técnicas
                    if agent_msg.get("toolCalls"):
                        silent_turns += 1
                    else:
                        break # El agente no hizo trabajo técnico, racha rota.
                i -= 2 # Saltar al siguiente par User-Gemini
            else:
                i -= 1

        output = {"status": "proceed"}
        
        if silent_turns >= THRESHOLD:
            msg = f"VIGILANCIA RELACIONAL: Llevas {silent_turns} turnos de ejecución sin un diálogo profundo. ¿Estamos alineados? Considera presentar evidencia antes de seguir."
            output["systemMessage"] = f"[\033[93m! RELATIONAL SILENCE\033[0m] {msg}"
            output["hookSpecificOutput"] = {
                "additionalContext": f"ALERTA DE ABSORCIÓN: Has realizado {silent_turns} ciclos de ejecución técnica con feedback mínimo. El PEG v2.1 sugiere una pausa socrática para validar el rumbo con Marcelo."
            }
        
        print(json.dumps(output))

    except Exception as e:
        sys.stderr.write(f"Error en delivery-discipline hook (refactor): {str(e)}\n")
        print(json.dumps({"status": "error_but_proceed", "error": str(e)}))

if __name__ == "__main__":
    main()
