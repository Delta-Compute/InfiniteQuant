Deployment of Infinite Quant App

✅ 1. Backend (FastAPI + Celery + Redis via Docker)

Run From Project Root:
Make sure you’re in the folder where your docker-compose.yml file lives:

'cd ~/infinite-quant  # or your actual backend project root'

Start the backend stack:
'docker compose up --build'

This will:

Start FastAPI (http://localhost:8000)
Start Celery worker (background backtest runner)
Start Redis (queue broker)


✅ 2. Frontend (React + Vite)

💡 In another terminal window:
Navigate to your frontend folder:

'cd ~/infinite-quant-frontend'  # or wherever your frontend lives

Install dependencies:
'npm install'

Run the local dev server:
'npm run dev'

You’ll see something like:

Local: http://localhost:5173

Open that in your browser and you’re live ✅
