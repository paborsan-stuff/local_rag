# README_PLUS

## Descripción General
Este documento resume y proporciona instrucciones detalladas para ejecutar la aplicación, desde el arranque del servidor Python (FastAPI) hasta la ejecución del front-end en DesktopAssistant utilizando npm.

## Flujo de Ejecución del Sistema
1. **Backend (Servidor Python)**
   - Se arranca con `python api_server.py`. Este servidor utiliza FastAPI para exponer el endpoint `/api/ask`.
   - El endpoint en `api_server.py` recibe solicitudes de la UI, valida el prompt y llama a la función `answer_query` en `src/rag.py` para procesar y generar la respuesta.
2. **Interfaz de Usuario (DesktopAssistant)**
   - La UI se encuentra en la carpeta `DesktopAssistant` y se ejecuta usando `npm run dev` mediante Vite.
   - El componente `PromptInput.jsx` captura el prompt del usuario y envía una solicitud POST al endpoint `/api/ask`.
   - La respuesta del backend, recibida en `OutputDisplay.jsx`, se muestra en la caja de chat para el usuario.

## Instrucciones para Ejecutar la Aplicación
1. **Ejecutar el Servidor Python:**
   - Asegúrate de tener instaladas todas las dependencias de Python y configurado el entorno correctamente.
   - Desde la raíz del proyecto, ejecuta:
     ```bash
     python api_server.py
     ```
   - Esto levantará el servidor en `http://localhost:8000`.

2. **Ejecutar la Interfaz de Usuario:**
   - Abre una nueva terminal y navega al directorio `DesktopAssistant`:
     ```bash
     cd DesktopAssistant && npm run dev
     ```
   - La aplicación se levantará y podrá ser visualizada en el navegador en `http://localhost:3000`.

## Comentarios Adicionales en el Código
- **api_server.py:**  
  - Define el endpoint `/api/ask` que recibe y procesa el prompt de la UI, y llama a `answer_query` en `src/rag.py` para manejar la lógica de respuesta.
- **src/rag.py:**  
  - Actualmente, la función `answer_query` está hardcodeada para devolver "Testing", facilitando la verificación de la conexión entre la UI y el backend.
- **DesktopAssistant/src/components/PromptInput.jsx:**  
  - Captura el input del usuario y realiza una solicitud fetch a `/api/ask`, enviando el prompt al backend.
- **DesktopAssistant/vite.config.js:**  
  - Configura un proxy que redirige las peticiones con el prefijo `/api` a `http://localhost:8000`, permitiendo la comunicación correcta entre el front-end y el servidor Python.

Este documento complementa el README principal y sirve como una guía rápida tanto para entender la integración entre los componentes del sistema como para probar la conexión completa desde el servidor Python hasta la interfaz en React.
