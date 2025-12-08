# SaaS Quickstart

Vue 3 + FastAPI + Supabase starter template.

## Stack

- **Frontend**: Vue 3, TypeScript, Tailwind CSS, shadcn-vue
- **Backend**: FastAPI (Python)
- **Auth**: Supabase

## Setup

### 1. Install dependencies
```bash
npm run install-all
```

### 2. Configure environment

**Frontend** (`frontend/.env`):
```
VITE_SUPABASE_URL=http://127.0.0.1:54321
VITE_SUPABASE_ANON_KEY=your_anon_key
VITE_BACKEND_URL=http://127.0.0.1:8000
```

**Backend** (`backend/.env`):
```
ENVIRONMENT=development
FRONTEND_URL=http://localhost:5173
```

### 3. Start Supabase (local)
```bash
supabase start
supabase status  # Get your anon key
```

### 4. Run dev servers
```bash
npm run dev
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

## License

MIT
