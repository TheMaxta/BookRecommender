# Simple App Documentation

## Project Structure
```
project/
├── frontend/     # Frontend application
└── backend/      # Backend server
```

## Getting Started

### Backend
Navigate to the backend directory:
```bash
cd backend
```

Start the backend server:
```bash
poetry run uvicorn bookdataset.api.endpoints:app --host 0.0.0.0 --port 5001 --reload
```

### Frontend 
Navigate to the frontend directory:
```bash
cd frontend
```

Start the frontend development server:
```bash
npm run dev
```

### Access the Application
Once both servers are running, access the application at:
```
http://localhost:3000
```