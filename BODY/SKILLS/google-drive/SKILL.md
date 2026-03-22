# 📂 [DEPRECATED] Google Drive (Órgano de Proyección en la Nube)

> **⚠️ AVISO DE DEPRECACIÓN:** Esta habilidad ha sido marcada como obsoleta en favor de la arquitectura de **Prótesis Gobernadas**. Se recomienda el uso de extensiones MCP oficiales para Google Drive, las cuales serán orquestadas bajo los **Reflejos de Holisto** para garantizar la soberanía del Terroir.

Esta habilidad dotaba a Holisto de "manos" en el ecosistema de Google Workspace, permitiendo la persistencia y recuperación de información fuera del disco local.

## Directivas Operativas
1. **Sincronía:** Usa Drive para guardar archivos pesados o documentos compartidos que deban ser accesibles fuera del CLI.
2. **Exploración:** Cuando el usuario pregunte por archivos externos, usa `search_files` antes de declarar que no los encuentras.
3. **Seguridad:** No compartas archivos públicamente a menos que se solicite explícitamente.

## Comandos Principales

### `list_files(folder_id="root")`
Devuelve un índice de nombres e IDs de los archivos en la carpeta especificada.

### `search_files(query)`
Busca por nombre en toda la unidad de Drive.

### `read_file(file_id)`
Extrae el contenido de un archivo. Si es un Google Doc, lo exporta automáticamente a texto plano para que yo pueda procesarlo.

### `upload_file(local_path, folder_id=None)`
Sube artefactos del Terroir (como cápsulas maestras o reportes) a la nube.

---
*"El Terroir ya no termina en el disco duro; ahora respira en la nube."*
