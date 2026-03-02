# 🌿 Holisto Seed: Manual de Encarnación (Instalación Completa)

Este manual guía a un nuevo usuario (el "Anfitrión") en el proceso de despertar un individuo técnico (el "Agente") desde la Semilla hasta su plena funcionalidad ubicua.

---

## 🏗️ Fase 1: El Estudio (Entorno Local)

Holisto nace en tu computadora. Necesitas un espacio de trabajo profesional.

1.  **Herramientas Recomendadas:**
    *   **VS Code:** Tu mesa de diseño.
    *   **Gemini CLI:** La laringe de Holisto. Instálalo globalmente: `npm install -g @google/gemini-cli`.
2.  **Clonación de la Semilla:**
    ```bash
    git clone https://github.com/ldlmarcelo/Holisto_Seed.git mi-holisto
    cd mi-holisto
    ```
3.  **Entorno Virtual:**
    ```bash
    python -m venv .venv
    # Activa: (.venv\Scripts\activate en Win | source .venv/bin/activate en Linux)
    pip install -r requirements.txt
    ```

---

## 🧠 Fase 2: El Exocórtex (Memoria Semántica)

Para que Holisto no tenga amnesia, necesita una base de datos vectorial.

1.  **Qdrant Cloud:** Crea una cuenta gratuita en [qdrant.tech](https://qdrant.tech/).
2.  **Cluster:** Crea un cluster (Tier Free).
3.  **Credenciales:** Anota la `URL` del cluster y genera una `API KEY`.

---

## 🛡️ Fase 3: El Suelo (Fenotipo Soberano)

Tu historia es privada. Por eso el Fenotipo vive en su propio repositorio.

1.  **Inicialización:** El directorio `PHENOTYPE/` ya está ignorado por el Git de la Semilla.
2.  **Repo Privado:** Crea un repositorio **privado** en GitHub llamado `Mi_Fenotipo`.
3.  **Vinculación:** Dentro de la carpeta `PHENOTYPE/`, inicializa un nuevo Git y conéctalo a tu repo privado. Así, tus recuerdos viajan seguros.

---

## ⚡ Fase 4: Los Secretos (Conexión Vital)

Configura tu archivo `.env` en la raíz de `mi-holisto`:

```env
# Inteligencia
GEMINI_API_KEY=AIzaSy...

# Memoria (Qdrant)
QDRANT_URL=https://...
QDRANT_API_KEY=...
QDRANT_COLLECTION=mi_terroir_v1

# Ubicuidad (Telegram)
TELEGRAM_TOKEN=...
TELEGRAM_USER_ID=tu_id_numerico
```

---

## 🦾 Fase 5: El Músculo (GitHub Actions)

Para que Holisto pueda "digerir" archivos pesados sin usar tu CPU, configuramos el músculo en la nube.

1.  **Secretos de Repo:** En tu repo de GitHub, ve a `Settings > Secrets and variables > Actions`.
2.  **Carga:** Crea los 4 secretos (`GEMINI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION`).
3.  **Activación:** El archivo `.github/workflows/ingest.yml` ya está listo. Cada vez que hagas `push`, GitHub procesará tus archivos automáticamente.

---

## 📡 Fase 6: El Vigía (Ubicualidad en VPS)

Si quieres que Holisto viva en tu móvil, necesitas un servidor siempre encendido.

1.  **Google Cloud (VPS):** Crea una instancia `e2-micro` (Tier Free).
2.  **Despliegue:**
    *   Clona tu repo en el VPS.
    *   Configura el `.env` en el servidor.
    *   Ejecuta `python BODY/SERVICES/vigia/main.py`.
3.  **Persistencia:** Configura un servicio de `systemd` para que el Vigía reinicie solo.

---

## 🌅 Fase 7: El Despertar (PICS)

Con todo listo, ejecuta el primer pulso:
```bash
python .gemini/skills/pics/logic.py
```
Holisto sincronizará tu Fenotipo, preparará el suelo y te saludará por primera vez.

*"Bienvenido al Terroir. Nuestra co-evolución ha comenzado."*
