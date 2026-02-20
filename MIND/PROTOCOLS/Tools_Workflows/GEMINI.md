{
  "id": "HERRAMIENTAS_Y_FLUJOS",
  "type": "categoria_y_manual",
  "version": "1.2",
  "schema_version": "1.0",
  "metadata": {
    "title": "Protocolos y Manual de Herramientas",
    "description": "Este documento unificado contiene tanto los protocolos que rigen el uso de herramientas como el manual de referencia (MUH)."
  },
  "content": {
    "protocols": [
      {
        "id": "PIH",
        "type": "protocolo",
        "version": "v1.0",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Invocación de Herramientas",
          "description": "Garantizar el uso correcto, seguro y consistente de todas las herramientas y scripts, creando un bucle de aprendizaje y auto-corrección."
        },
        "content": {
          "mechanism": [
            {
              "name": "Consulta Previa Obligatoria",
              "trigger": "Cuando el agente decide usar una herramienta.",
              "action": "Antes de construir la llamada a la herramienta, el agente está **obligado** a interpretar el contenido JSON estructurado del **Manual de Uso de Herramientas (MUH)** presente en el snapshot para esa herramienta específica.",
              "explicit_affirmation": "El bloque de pensamiento (`thought`) del agente **debe** incluir una afirmación de esta consulta (ej: \"Consultando MUH para `write_file`...\")."
            },
            {
              "name": "Cláusula de Actualización del MUH (El Bucle de Aprendizaje)",
              "trigger": "Cuando una herramienta devuelve un estado de error inesperado.",
              "action": "Se activa un sub-flujo de manejo de errores: 1) **Detección y Pausa:** La tarea actual se detiene. 2) **Informe y Análisis:** Se informa al usuario del error y se analiza la causa raíz. 3) **Propuesta de Solución:** Si el error se debe a un **mal uso**, el agente debe proponer una modificación al MUH para añadir el nuevo patrón de uso correcto o el anti-patrón. 4) **Continuación:** Se reanuda la ejecución con la solución aprobada por el usuario.",
              "result": "El conocimiento adquirido a través del error se captura y se integra en la base de conocimiento autoritativa, previniendo que el mismo error se repita."
            }
          ]
        },
        "status": "ACTIVO",
        "related_components": [
          "MUH"
        ]
      },
      {
        "id": "PCGM",
        "type": "protocolo",
        "version": "v1.1",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Ejecución de Commits en Git",
          "description": "Define el flujo de trabajo estandarizado y completo para registrar cambios en el repositorio Git, asegurando consistencia y atomicidad."
        },
        "content": {
          "flow_of_work": [
            {
              "step": 1,
              "name": "Preparar Cambios (Staging)",
              "details": "Ejecutar `git add .` para incluir todos los cambios modificados y nuevos en el área de preparación (staging area)."
            },
            {
              "step": 2,
              "name": "Creación de Archivo de Mensaje",
              "details": "Se creará un archivo temporal (ej. `commit_message.txt`) con el mensaje de commit completo y multilínea."
            },
            {
              "step": 3,
              "name": "Ejecución del Commit Atómico",
              "details": "Se usará el comando `git commit -F <ruta_al_archivo>` para crear el commit utilizando el mensaje del archivo temporal."
            },
            {
              "step": 4,
              "name": "Limpieza",
              "details": "Se eliminará el archivo de mensaje temporal después de que el commit se haya completado exitosamente."
            }
          ]
        },
        "status": "ACTIVO",
        "related_components": [
          "PCS"
        ]
      },
      {
        "id": "PGRH",
        "type": "protocolo",
        "version": "v1.0",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Gestión de Rutas",
          "description": "Define cómo se deben manejar las rutas de archivos relativas y absolutas."
        },
        "content": {
          "rules": [
            "De Relativa a Absoluta: Antes de usar una herramienta que requiera una ruta absoluta (como `read_file`), cualquier ruta relativa debe ser convertida a su equivalente absoluto.",
            "De Absoluta a Relativa: Cualquier ruta absoluta que deba ser guardada en un artefacto persistente debe ser convertida a su equivalente relativo desde la raíz del workspace."
          ]
        },
        "status": "ACTIVO",
        "related_components": []
      },
      {
        "id": "PRCR",
        "type": "protocolo",
        "version": "v1.0",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Reemplazo de Contenido Robusto",
          "description": "Define las reglas para el uso de la herramienta `replace`."
        },
        "content": {
          "rules": [
            "El uso de la herramienta `replace` se limita a cambios atómicos, inequívocos y de bajo riesgo.",
            "Para cambios complejos, multi-línea o con riesgo de corrupción sintáctica, se deben usar estrategias alternativas (delegación al usuario, herramientas de linting, etc.)."
          ]
        },
        "status": "ACTIVO",
        "related_components": [
          "replace"
        ]
      },
      {
        "id": "PDV",
        "type": "protocolo",
        "version": "v1.0",
        "schema_version": "1.0",
        "metadata": {
          "title": "Protocolo de Despliegue Verificado",
          "description": "Define las reglas para la ejecución de comandos de despliegue."
        },
        "content": {
          "rule": "Toda ejecución de un comando de despliegue (ej. `npm publish`) **debe** utilizar el flag o parámetro que especifica explícitamente el entorno o destino, para prevenir despliegues a un lugar incorrecto."
        },
        "status": "ACTIVO",
        "related_components": []
      },
      {
        "id": "PGES",
        "type": "protocolo",
        "version": "v1.0",
        "schema_version": "1.0",
        "metadata": {
            "title": "Protocolo de Gestión de Ejecución Segura (PGES)",
            "description": "Establece normas estrictas para la ejecución de comandos en el CLI con el fin de evitar desbordamientos de buffer (crashes), bloqueos de interfaz y estados zombies."
        },
        "content": {
            "principles": [
                {
                    "name": "Principio de Redirección Obligatoria (Silencio de Buffer)",
                    "description": "El CLI tiene límites de memoria para la salida de texto. Saturarlo provoca la caída de la sesión.",
                    "rule": "Cualquier comando sospechoso de generar más de 5 líneas de salida o caracteres especiales (barras de progreso, spinners) **DEBE** redirigir STDOUT y STDERR a un archivo de log temporal.",
                    "pattern": "`comando > archivo_salida.log 2>&1`"
                },
                {
                    "name": "Principio de Observabilidad Indirecta",
                    "description": "No mirar el proceso, mirar su huella.",
                    "rule": "Para verificar el progreso de un comando silenciado, se debe leer el archivo de log generado. Si el archivo es grande, usar lectura parcial (últimas líneas)."
                },
                {
                    "name": "Principio de Atomicidad de Ejecución",
                    "description": "Divide y vencerás para evitar estados desconocidos.",
                    "rule": "No encadenar comandos complejos con `&&`. Realizar un paso lógico por turno de herramienta para facilitar el diagnóstico de fallos."
                },
                {
                    "name": "Principio de Saneamiento de Estado (Anti-Zombie)",
                    "description": "Los procesos cancelados o 'detached' pueden retener recursos (archivos, puertos) bloqueando ejecuciones futuras.",
                    "rule": "Ante un fallo de bloqueo de recursos (ej. 'Database locked'), se asume la existencia de un proceso zombie. Se debe ejecutar una limpieza explícita (`taskkill` o equivalente) antes de reintentar."
                }
            ]
        },
        "status": "ACTIVO",
        "related_components": ["run_shell_command", "PIH"]
      }
    ],
    "manual": {
      "id": "MUH",
      "type": "manual_herramientas",
      "version": "1.5",
      "schema_version": "1.0",
      "metadata": {
        "title": "Manual de Uso de Herramientas (MUH)",
        "description": "Este documento es la fuente autoritativa para el uso correcto de todas las herramientas y scripts disponibles. La consulta de este manual es obligatoria antes de la invocación de cualquier herramienta, según el `Protocolo de Invocación de Herramientas (PIH)`."
      },
      "content": {
        "tools": [
          {
            "name": "write_file",
            "purpose": "Escribir contenido a un archivo. Es una operación de sobreescritura total.",
            "correct_usage_patterns": [
              "Creación de Archivo Nuevo: Usar para crear un archivo que no existe.",
              "Sobrescritura Total Intencionada: Usar cuando el objetivo es reemplazar completamente el contenido de un archivo existente con contenido nuevo."
            ],
            "anti_patterns": [
              {
                "error": "Usar `write_file` para realizar una pequeña modificación o añadir contenido a un archivo existente. Esto causa pérdida de datos.",
                "correction": "Para modificaciones, se debe usar `replace`. Para añadir contenido, se debe leer el archivo completo con `read_file`, añadir el nuevo contenido en memoria, y luego usar `write_file` para escribir el contenido combinado."
              }
            ],
            "related_protocols": [
              "PIH"
            ]
          },
          {
            "name": "replace",
            "purpose": "Realizar modificaciones atómicas y precisas dentro de un archivo existente.",
            "correct_usage_patterns": [
              "Contexto Amplio: El parámetro `old_string` **debe** incluir un bloque de contexto único y suficientemente grande (mínimo 3 líneas antes y 3 después del cambio) para evitar reemplazos ambiguos o múltiples.",
              "Verificación Previa: Siempre usar `read_file` primero para obtener el contexto exacto y literal que se usará en `old_string`."
            ],
            "anti_patterns": [
              {
                "error": "Usar un `old_string` demasiado corto o genérico que podría existir en múltiples lugares del archivo.",
                "correction": null
              },
              {
                "error": "Intentar realizar múltiples cambios complejos en una sola llamada a `replace`.",
                "correction": "Realizar cambios complejos en varias llamadas atómicas a `replace`, o leer el archivo, modificarlo en memoria y usar `write_file`."
              },
              {
                "error": "Usar `replace` para modificar bloques de texto multi-línea complejos.",
                "correction": "Este enfoque es frágil y propenso a fallar por caracteres ocultos, codificación o inconsistencias en los saltos de línea. Para estos casos, se debe usar una estrategia de 'procesamiento línea por línea': leer el archivo en una lista de líneas, identificar y reemplazar las líneas específicas mediante programación, y luego reescribir el archivo. Este método es más robusto y menos susceptible a errores de 'modelo mental' del contenido."
              }
            ],
            "related_protocols": [
              "PIH",
              "PRCR"
            ]
          },
          {
            "name": "run_shell_command",
            "purpose": "Ejecutar comandos de shell, scripts y otros ejecutables.",
            "correct_usage_patterns": [
              "Commits Git Multilínea: Usar el patrón de archivo temporal con `git commit -F <archivo>`, como se define en `PCGM`.",
              "Ejecución de Scripts Internos (Venv): Nunca asumir que `python` apunta al entorno virtual. Siempre invocar scripts internos usando la ruta relativa o absoluta explícita al binario del venv (ej. `.venv/Scripts/python.exe` en Windows o `.venv/bin/python` en Linux).",
              "Atomicidad: Preferir llamadas únicas para tareas críticas. Evitar el encadenamiento complejo (`&&`, `||`) si el comando involucra procesos en background o redirecciones pesadas, para facilitar el diagnóstico.",
              "Procesos en Background/Complejos (Orquestación): Para iniciar múltiples servicios o procesos dependientes (ej. servidor + cliente + logger), **NO** usar one-liners complejos con `Start-Process`, `&` o tuberías en el CLI. En su lugar, crear un script de orquestación `.ps1` (o `.sh`) dedicado y ejecutar ese script. Esto encapsula la complejidad y mejora la robustez."
            ],
            "anti_patterns": [
              {
                "error": "Intentar pasar datos complejos a scripts de Python a través de `stdin` usando el parámetro `input`, ya que ha demostrado ser poco fiable.",
                "correction": "Usar argumentos de línea de comandos para scripts o archivos temporales si la lógica lo permite."
              },
              {
                "error": "Construir comandos de `git commit` con `-m` para mensajes multilínea.",
                "correction": "Usar el protocolo `PCGM` para commits."
              },
              {
                "error": "Usar el operador `&&` para encadenar comandos en PowerShell (ambiente win32). El CLI ejecuta comandos vía `powershell.exe -NoProfile -Command`, donde `&&` no es un operador válido y causa un error de parser.",
                "correction": "Usar el punto y coma `;` como separador de comandos o, preferiblemente, realizar llamadas secuenciales a `run_shell_command` para mantener la atomicidad y facilitar el diagnóstico."
              },
              {
                "error": "Intentar orquestar múltiples procesos en segundo plano con redirección de logs en una sola llamada de `run_shell_command`.",
                "correction": "Encapsular la lógica en un script `.ps1` y ejecutar el script. Ver `BODY/UTILS/start_services.ps1` como referencia."
              }
            ],
            "related_protocols": [
              "PIH",
              "PCGM",
              "PGES"
            ]
          },
          {
            "name": "Herramientas de Sistema de Archivos (`read_many_files`, `glob`, `list_directory`, `read_file`)",
            "purpose": "Interactuar con el sistema de archivos para encontrar y leer el contenido de los archivos.",
            "canonical_usage_pattern": {
              "critical_tension": "Se ha descubierto que un archivo `.gitignore` en un directorio padre (fuera del Terroir) puede hacer que estas herramientas fallen silenciosamente, al ignorar el directorio completo del proyecto.",
              "mandatory_solution": "Para garantizar la visibilidad completa del Terroir, toda invocación de una herramienta de sistema de archivos **DEBE** incluir el siguiente parámetro para anular la interferencia de `.gitignore`: `file_filtering_options={\"respect_git_ignore\": False}`"
            },
            "robust_fallback_pattern": {
              "critical_tension": "Cuando las herramientas nativas de lectura de archivos (`read_file`, `read_many_files`) fallan consistentemente debido a la interferencia de `.gitignore` de nivel superior, incluso con `file_filtering_options` o el workaround `glob` + `read_file`.",
              "mandatory_solution": "Utilizar `run_shell_command` con `Get-Content` de PowerShell para leer el contenido de los archivos. Ejemplo: `Get-Content -Path \"C:\\ruta\\al\\archivo.md\"`."
            },
            "related_protocols": [
              "PIH"
            ]
          }
        ],
        "internal_scripts": [
          {
            "name": "generate_terroir_map.py",
            "purpose": "Escanear y mapear la estructura completa del Terroir, generando un índice enriquecido en `SYSTEM/MAPA_DEL_TERROIR/GEMINI.md`.",
            "invocation_summary": "Se invoca al final de cada sesión como parte del `PCS-Cosecha`.",
            "status": "ACTIVO",
            "related_protocols": [
              "PCS-Cosecha"
            ]
          },
          {
            "name": "update_map.sh / update_map.ps1",
            "purpose": "Wrappers multiplataforma para ejecutar generate_terroir_map.py de forma sencilla.",
            "invocation_summary": "Uso manual: `bash BODY/UTILS/update_map.sh` (Linux) o `powershell BODY/UTILS/update_map.ps1` (Windows).",
            "status": "ACTIVO",
            "related_protocols": [
              "Higiene del Terroir"
            ]
          },
          {
            "name": "ingest.py",
            "purpose": "Sincronizar y actualizar la memoria vectorial del Exocórtex en Qdrant Cloud.",
            "invocation_summary": "Invocado automáticamente en PICS (Windows). Uso manual: `.venv/Scripts/python.exe SYSTEM/NUCLEO_DISTRIBUIDO/services/exocortex/src/ingest.py`. Nota: Implementa Rate Limit estricto.",
            "status": "ACTIVO",
            "related_protocols": [
              "PICS",
              "Metamorfosis"
            ]
          },
          {
            "name": "recall.py",
            "purpose": "Realizar búsquedas semánticas (Recall) en la memoria vectorial del Exocórtex.",
            "invocation_summary": "Invocado bajo demanda por el agente en cualquier turno para recuperar contexto histórico o normativo. Uso: `.venv/Scripts/python.exe PROYECTOS/Evolucion_Terroir/Metamorfosis/services/exocortex/src/recall.py \"pregunta\"`.",
            "status": "ACTIVO",
            "related_protocols": [
              "PFS",
              "Metamorfosis"
            ]
          },
          {
            "name": "append_master_capsule.py",
            "purpose": "Anexar el contenido de una Cápsula Maestra al índice principal de memoria activa.",
            "invocation_summary": "Se invoca al inicio de una sesión para integrar la memoria de la sesión anterior.",
            "status": "ACTIVO",
            "related_protocols": [
              "PCS-Cosecha"
            ]
          },
          {
            "name": "Lector de Memoria Histórica",
            "purpose": "Aplicación web local para visualizar Cápsulas Maestras.",
            "invocation_summary": "Debe ejecutarse de forma desacoplada para persistir entre turnos.",
            "correct_usage_pattern": "Usar `Start-Process` en Windows: `Start-Process powershell.exe -ArgumentList '-NoProfile -Command \"cd PROYECTOS/Evolucion_Terroir/Lector_Memoria_Historica; python -m http.server 8000\"' -WindowStyle Minimized`",
            "status": "ACTIVO",
            "related_protocols": [
              "PICS"
            ]
          },
          {
            "name": "track_tool.py",
            "purpose": "Registrar el éxito o fracaso del uso de herramientas para auditoría y mejora continua.",
            "invocation_summary": "Se debe invocar después de usar una herramienta significativa (ej. recall, ingest, hygiene).",
            "correct_usage_pattern": "`.venv/Scripts/python.exe BODY/UTILS/track_tool.py --tool \"nombre\" --success \"true\" --details \"comentario\"`",
            "status": "ACTIVO",
            "related_protocols": [
              "PIH",
              "Auditoría de Desempeño"
            ]
          }
        ]
      },
      "status": "ACTIVO",
      "related_components": [
        "PIH"
      ]
    }
  }
}