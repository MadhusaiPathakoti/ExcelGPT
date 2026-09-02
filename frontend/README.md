# ExcelGPT Frontend

React + TypeScript SPA for ExcelGPT, built with Vite, Tailwind CSS, and Recharts. Talks to the FastAPI backend in [`../backend`](../backend) over the REST API defined there.

## Setup

```bash
npm install
cp .env.example .env   # then edit VITE_API_BASE_URL if needed
npm run dev
```

`VITE_API_BASE_URL` defaults to `http://localhost:8000/api`. Point it at the deployed backend URL (see `../backend/render.yaml`) for production builds.

## Scripts

- `npm run dev` — start the Vite dev server
- `npm run build` — type-check (`tsc -b`) and produce a production build in `dist/`
- `npm run preview` — serve the production build locally
- `npm run lint` — run oxlint

## Structure

- `src/api/` — typed fetch client and API response types
- `src/components/` — UI components (upload, dataset overview, chat, charts)
- `src/lib/` — chart data transforms (pivoting, CSV export, treemap/heatmap shaping)
- `src/types/` — chat message types
