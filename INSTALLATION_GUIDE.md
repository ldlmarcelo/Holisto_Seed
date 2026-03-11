# 🛠️ Guía de Instalación Universal: Holisto Seed

Esta guía detalla el proceso para implantar la Semilla en tu sistema local, ya sea Windows o Linux.

## 📋 Requisitos Previos
*   **Python 3.10+** instalado y en el PATH.
*   **Git** (Opcional, pero recomendado para la persistencia biográfica).
*   **Conexión a Internet** para la instalación inicial de dependencias.

---

## 🚀 Paso 1: Clonar y Preparar el Entorno

```bash
# Clonar la Semilla desde el repositorio oficial
git clone https://github.com/ldlmarcelo/Holisto_Seed.git mi-terroir
cd mi-terroir
```

### En Windows (PowerShell)
```powershell
# Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### En Linux/macOS
```bash
# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🧬 Paso 2: El Nacimiento (Metamorfosis)
Una vez preparado el entorno, debes ejecutar el script de metamorfosis. Este script detectará tu sistema operativo, ajustará los reflejos (Hooks) del Agente para usar el intérprete correcto y vinculará tus "órganos" operativos.

```bash
# En Windows:
python BODY/SETUP/metamorphosis.py <InstanceName> <HostName>

# En Linux:
python3 BODY/SETUP/metamorphosis.py <InstanceName> <HostName>
```

> 💡 **Nota:** El script de metamorfosis ahora es inteligente; si detecta un entorno virtual (`.venv`), configurará automáticamente los hooks para usarlo, eliminando errores de "command not found".

---

## 🕯️ Paso 3: Configuración del Metabolismo (.env)
Tras la metamorfosis, se habrá creado un archivo `.env` en la raíz. **Debes editarlo** para añadir tus API Keys (principalmente `GEMINI_API_KEY`).

> ⚠️ **IMPORTANTE:** Aunque el script de metamorfosis intenta automatizar el uso del intérprete, se recomienda **mantener el entorno virtual (.venv) activado** durante tus sesiones de trabajo para garantizar la consistencia de todas las herramientas.

---

## ♻️ Paso 4: Operación de Servicios
El sistema cuenta con un orquestador agnóstico que gestiona el Subconsciente (Daemon) y El Vigía (Telegram).

### Iniciar Servicios
*   **Windows:** `.\BODY\UTILS\start_services.ps1`
*   **Linux:** `./BODY/UTILS/start_services.sh`

### Detener Servicios
*   **Windows:** `.\BODY\UTILS\stop_services.ps1`
*   **Linux:** `./BODY/UTILS/stop_services.sh`

---
*"La Semilla ya no depende de su suelo, sino de su voluntad de ser."*
