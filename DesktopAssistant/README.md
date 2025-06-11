# DesktopAssistant

DesktopAssistant is a desktop web interface built with React and Tailwind CSS. Inspired by Apple's design aesthetic, this application is clean, modern, and minimalist. **Note:** The interface is designed exclusively for desktop and is not responsive.

## Requirements

- Node.js (Latest LTS version)
- npm

## Installation

From the project root directory:
```bash
cd DesktopAssistant
npm install
```

## Development Execution

```bash
npm run dev
```

This will start the application at [http://localhost:3000](http://localhost:3000).

## Production Build

```bash
npm run build
```

## Notes

- Vite is used as the build tool.
- Tailwind CSS is configured through PostCSS.
- The application calls the API at `/api/ask` when submitting a prompt and displays the response.

## How to Test the UI

To test the user interface, run the following command from the project root:
```bash
npm run dev
```
Then, open your browser and navigate to [http://localhost:3000](http://localhost:3000) to view the application.
