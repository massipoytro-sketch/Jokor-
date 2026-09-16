# Jokor Frontend

Vite + React single-page interface for the Jokor Free Fire player-information platform.

## Local development

```bash
cd frontend
npm install
npm run dev
```

## API connection

Set `VITE_API_URL` to the public URL of the Jokor Flask backend. If it is omitted, the frontend uses same-origin `/api/...` requests.

Example:

```env
VITE_API_URL=https://your-jokor-api.onrender.com
```

## Production

```bash
npm run build
```

The production output is generated in `dist/` and can be deployed to Vercel or another static hosting service.

The backend is deployed separately through the repository root `render.yaml`, which points Render at `backend/`.

## Included tools

- Player UID scan
- BR / CS statistics view
- Player comparison
- Nickname search
- Guild lookup
- Game/rank metadata
- API/system status
- Responsive ion-green / black Jokor visual system
