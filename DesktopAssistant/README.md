# DesktopAssistant

DesktopAssistant es una interfaz web de escritorio construida con React y Tailwind CSS. Inspirada en el look and feel de la web de Apple, esta aplicación es limpia, moderna y minimalista. **Nota:** La interfaz es solamente para escritorio y no es responsive.

## Requisitos

- Node.js (última versión LTS)
- npm

## Instalación

Desde el directorio raíz del proyecto:
```bash
cd DesktopAssistant
npm install
```

## Ejecución en Desarrollo

```bash
npm run dev
```

Esto iniciará la aplicación en [http://localhost:3000](http://localhost:3000).

## Construir para Producción

```bash
npm run build
```

## Notas

- Se utiliza Vite como herramienta de construcción.
- Tailwind CSS está configurado vía PostCSS.
- La aplicación realiza una llamada a la API en `/api/ask` al enviar el prompt y muestra la respuesta.

## Cómo probar la UI

Para probar la interfaz de usuario, ejecuta el siguiente comando en la raíz del proyecto:
```bash
npm run dev
```
Luego, abre tu navegador y visita [http://localhost:3000](http://localhost:3000) para ver la aplicación.
