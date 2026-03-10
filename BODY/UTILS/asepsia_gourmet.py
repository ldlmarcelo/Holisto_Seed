import json
import os
import sys

def filter_log_gourmet(log_entries):
    """
    Realiza una asepsia narrativa profunda: 
    - Elimina toolCalls y toolOutputs masivos.
    - Trunca partes de texto excesivamente largas (>5000 chars).
    - Preserva la narrativa dialógica esencial.
    """
    clean_messages = []
    if not isinstance(log_entries, list):
        return clean_messages

    for entry in log_entries:
        if not isinstance(entry, dict): continue
            
        new_msg = {"role": entry.get("role", "unknown"), "content": ""}
        content = entry.get("content")
        
        if isinstance(content, list):
            text_parts = []
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    text = part["text"]
                    if len(text) > 5000:
                        text_parts.append(text[:1000] + f"\n... [TRUNCADO: {len(text)} caracteres de ruido técnico] ...\n" + text[-1000:])
                    else:
                        text_parts.append(text)
            new_msg["content"] = "\n".join(text_parts)
        elif isinstance(content, str):
            if len(content) > 5000:
                new_msg["content"] = content[:1000] + f"\n... [TRUNCADO: {len(content)} caracteres] ...\n" + content[-1000:]
            else:
                new_msg["content"] = content
        
        if new_msg["content"].strip():
            clean_messages.append(new_msg)
            
    return clean_messages

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python asepsia_gourmet.py <path_al_log_json>")
        sys.exit(1)
        
    input_p = sys.argv[1]
    if not os.path.exists(input_p):
        print(f"Error: {input_p} no existe.")
        sys.exit(1)
        
    with open(input_p, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, dict) and "messages" in data:
            data = data["messages"]
            
    clean = filter_log_gourmet(data)
    output_p = input_p.replace(".json", "_CLEAN.json")
    
    with open(output_p, 'w', encoding='utf-8') as f:
        json.dump(clean, f, indent=2, ensure_ascii=False)
    
    print(f"Asepsia completada: {output_p}")
    print(f"Reducción: {os.path.getsize(input_p)/1024/1024:.2f}MB -> {os.path.getsize(output_p)/1024/1024:.2f}MB")
