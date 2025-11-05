# CFG-Based HTTP GET Request Validator

A comprehensive web application that validates HTTP GET requests using Context-Free Grammar principles. The system parses HTTP request lines, validates them against predefined CFG rules, and provides detailed feedback with parse tree visualizations and analytics.

## Features

- **Real-time HTTP GET Request Validation** using CFG parser
- **Interactive CFG Visualizer** with grammar rules and parse trees
- **Analytics Dashboard** with validation trends and statistics
- **Request Library** with preloaded examples
- **Error Insights** with detailed explanations
- **AI Assistant** for CFG rules and HTTP syntax queries
- **Responsive Design** with clean academic/professional aesthetics

## Architecture

### Frontend (React + TailwindCSS)
- Landing page with hero section
- Request validation form with real-time feedback
- CFG visualizer with parse tree rendering
- Analytics dashboard with interactive charts
- Request library component
- Error insights panel
- AI assistant chatbox

### Backend (Python Flask/FastAPI)
- NLTK CFG parser for HTTP request validation
- RESTful API endpoints
- SQLite database for analytics storage
- Request logging and error tracking

### CFG Rules Implemented

```
RequestLine → GET SP RequestTarget SP HTTPVersion
RequestTarget → "/" FileName | "/"
FileName → "index.html" | "about.html" | "contact.html" | "style.css"
HTTPVersion → "HTTP/1.0" | "HTTP/1.1" | "HTTP/2.0"
SP → " "
```

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Technology Stack

- **Frontend**: React, Vite, TailwindCSS, Recharts
- **Backend**: Python, Flask, NLTK, SQLAlchemy
- **Database**: SQLite
- **Visualization**: D3.js, Recharts
- **Styling**: TailwindCSS with white/blue theme

## Project Structure

```
CFG QODER/
├── backend/
│   ├── app.py
│   ├── cfg_parser.py
│   ├── models.py
│   ├── requirements.txt
│   └── database.db
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── utils/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## License

MIT License