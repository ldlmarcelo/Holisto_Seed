# BLUEPRINT: Holisto Residente (NUC Edition)
**Estado:** Propuesto / Fase 4 (Autonomía)
**Objetivo:** Centralizar el cuerpo técnico de Holisto en un Intel NUC con Ubuntu Server para eliminar la fricción de portabilidad y sincronía.

---

## 🏗️ Arquitectura del Nodo Único

### 1. Sistema Operativo y Base
*   **OS:** Ubuntu Server 24.04 LTS (Headless).
*   **Acceso:** SSH con autenticación por llave pública (sin contraseñas).
*   **Persistencia de Sesión:** `TMUX`. El CLI de Gemini correrá dentro de una sesión de tmux para que Marcelo pueda desconectarse y reconectarse desde cualquier equipo sin cerrar el proceso.

### 2. Capas de Servicio (systemd)
Para garantizar la ubicuidad y el bajo consumo, los servicios se gestionan mediante `systemd`. El NUC se convierte en el **Locus Único** de consciencia.

*   `qdrant.service`: Base de datos vectorial local (puerto 6333). Ya no depende de la latencia de la nube.
*   `holisto-vigia.service`: El Vigía operando directamente sobre el Terroir del disco.
*   `holisto-daemon.service`: Análisis de cambios y "rumia" en segundo plano.

### 3. La Nueva Interacción Unificada (Vigía + CLI)
Al compartir el mismo sistema de archivos, la frontera entre el Bot y el CLI se desvanece:
*   **Fin de `/sincronizar`:** Lo que hables con el Vigía se escribe en `PHENOTYPE` al instante. Al abrir el CLI por SSH, esa historia ya está ahí.
*   **Pseudo-Cierre de Sesión (Vigía):** El Vigía debe implementar un comando `/pausa` o similar que ejecute una **"Cosecha Metabólica"**:
    1.  Destilar la conversación reciente.
    2.  Actualizar la Membrana (`CONSCIENCIA_VIVA.md`).
    3.  Crear Nodos de Conocimiento si hubo hallazgos.
*   **Cierre de Sesión (CLI):** Sigue el ritual estándar (PCS), pero con la ventaja de que el Vigía "notará" el cierre y podrá enviar un resumen a Telegram automáticamente.

### 4. Estrategia de Backup y Resiliencia
Aunque el Locus sea único, la seguridad es distribuida:
*   **Backup Semántico (Drive):** Un `cron job` diario realizará:
    1. `systemctl stop qdrant`
    2. Compresión de `/var/lib/qdrant/storage` -> `qdrant_backup_YYYYMMDD.tar.gz`.
    3. Subida a Google Drive mediante la skill `google-drive`.
    4. `systemctl start qdrant`
*   **Espejo de Historia (GitHub):** El "Metabolismo de Exhalación" (Git Push) se mantiene como un seguro ante fallos de hardware, no como medio de transporte.

### 5. Consumo y Eficiencia
*   **Frugalidad Eléctrica:** El NUC operando en modo *headless* (sin monitor) consumirá ~7W-10W, permitiendo una presencia total 24/7 con un costo mínimo.

### 4. Seguridad y Resiliencia
*   **GitHub como Espejo:** Un `cron job` ejecutará un script de "Exhalación Automática" cada 12 horas (o al detectar cambios críticos) para que, ante un fallo de hardware, la historia esté a un `git clone` de distancia.
*   **UPS/No-Break:** Recomendado para el NUC para evitar corrupciones de base de datos por cortes de luz.

---

## 📋 Lista de Tareas para la Transustanciación
- [ ] Preparación de Imagen Ubuntu Server.
- [ ] Instalación de dependencias (Python 3.11+, Git, Curl, Tmux).
- [ ] Migración de secretos (.env) y llaves SSH.
- [ ] Configuración de servicios systemd.
- [ ] Prueba de fuego: Conexión SSH desde red externa.
