# SmartBharat AI

India's First AI-Powered Civic Operating System. SmartBharat AI acts as a single intelligent interface between Indian citizens and government services, combining the features of a ChatGPT companion, DigiLocker, and a government service finder.

## Architecture

- **Frontend**: Next.js 15, React 19, Tailwind CSS v4, Shadcn UI, Framer Motion
- **Backend**: FastAPI, Python, LangGraph
- **Database**: PostgreSQL (via Supabase) with `pgvector`
- **AI Models**: Google Gemini 2.5 Flash / Pro (via `google-genai` SDK)

## Local Setup

### 1. Prerequisites
- Docker and Docker Compose
- Node.js 18+ (if running locally without Docker)
- Python 3.11+ (if running locally without Docker)

### 2. Environment Variables
Copy the example environment file and fill in your keys:
```bash
cp .env.example .env
```
Ensure `GEMINI_API_KEY` is set.

### 3. Running with Docker Compose
The easiest way to run the entire stack locally is using Docker Compose:
```bash
docker-compose up --build
```
This will start:
- **Frontend** on `http://localhost:3000`
- **Backend** on `http://localhost:8000`
- **PostgreSQL Database** on `localhost:5432`

## Deployment Guides

### Frontend (Vercel)
The Next.js frontend is optimized for deployment on Vercel.
1. Push your repository to GitHub.
2. Go to [Vercel](https://vercel.com/) and import the project.
3. Select the `frontend` directory as the Root Directory.
4. Add the `NEXT_PUBLIC_API_URL` environment variable (e.g., your Cloud Run URL).
5. Click **Deploy**.

### Backend (Google Cloud Run / Railway)
The FastAPI backend is fully Dockerized and stateless, making it perfect for Cloud Run or Railway.

**Option A: Railway (Easiest)**
1. Connect your GitHub repo to Railway.
2. Select the `backend` directory.
3. Railway will automatically detect the `Dockerfile` and build it.
4. Add your `GEMINI_API_KEY` and `DATABASE_URL` in the Variables tab.

**Option B: Google Cloud Run**
1. Build and submit the image to Google Container Registry (GCR):
   ```bash
   cd backend
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/smartbharat-backend
   ```
2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy smartbharat-backend \
     --image gcr.io/YOUR_PROJECT_ID/smartbharat-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars="GEMINI_API_KEY=your_key,DATABASE_URL=your_db_url"
   ```

## Database Initialization (Supabase)
For production, it is recommended to use Supabase.
Execute the contents of `backend/seed.sql` in your Supabase SQL Editor to initialize the `profiles`, `schemes`, and `complaints` tables.

## API Documentation
Once the backend is running, you can access the auto-generated Swagger UI documentation at:
`http://localhost:8000/docs`
# SmaratbharatAI
