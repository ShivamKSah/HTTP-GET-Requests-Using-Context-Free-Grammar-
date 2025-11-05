# CFG-Based HTTP GET Request Validator - Setup Guide

## Quick Start

This guide will help you set up and run the CFG-Based HTTP GET Request Validator application on your local machine.

## Prerequisites

- **Python 3.8+** (tested with Python 3.13)
- **Node.js 16+** (tested with Node 18+)
- **npm** or **yarn**
- **Git** (optional, for cloning)

## Installation

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd "CFG QODER"

# Or download and extract the zip file
```

### 2. Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
# On Windows
py -m pip install -r requirements.txt

# On macOS/Linux
python3 -m pip install -r requirements.txt
```

3. Start the backend server:
```bash
# On Windows
py app.py

# On macOS/Linux
python3 app.py
```

The backend will start on `http://localhost:5000`

### 3. Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## Using the Application

1. **Open your browser** and navigate to `http://localhost:5173`
2. **Explore the features:**
   - **Landing Page**: Overview and introduction
   - **Validator**: Test HTTP requests in real-time
   - **Grammar**: Learn about CFG rules
   - **Library**: Browse example requests
   - **Dashboard**: View analytics and statistics
   - **Errors**: Understand common validation errors

## Supported HTTP Requests

The validator supports HTTP GET requests with the following structure:

```
GET <request-target> HTTP/<version>
```

### Valid Components:

- **HTTP Method**: `GET` (case-sensitive)
- **Request Targets**:
  - `/` (root)
  - `/index.html`
  - `/about.html`
  - `/contact.html`
  - `/style.css`
- **HTTP Versions**: `HTTP/1.0`, `HTTP/1.1`, `HTTP/2.0`

### Example Valid Requests:
- `GET / HTTP/1.1`
- `GET /index.html HTTP/2.0`
- `GET /about.html HTTP/1.0`

### Example Invalid Requests:
- `POST /index.html HTTP/1.1` (wrong method)
- `GET /page.html HTTP/1.1` (invalid filename)
- `GET /index.html HTTP/3.0` (invalid version)

## Troubleshooting

### Backend Issues

1. **Import errors**: Make sure all dependencies are installed:
```bash
py -m pip install --upgrade -r requirements.txt
```

2. **Port already in use**: Change the port in `app.py`:
```python
port = int(os.environ.get('PORT', 5001))  # Change 5000 to 5001
```

3. **NLTK data missing**: The app should download required NLTK data automatically, but you can manually download:
```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```

### Frontend Issues

1. **Dependencies issues**: Clear node modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

2. **Port conflicts**: The frontend will automatically find an available port, usually `5173`

3. **API connection issues**: Check that the backend is running on `http://localhost:5000`

### Common Solutions

1. **CORS errors**: The backend includes CORS configuration, but if you encounter issues, check that both servers are running on the expected ports

2. **Path issues**: Make sure you're running commands from the correct directories (`backend/` for Python, `frontend/` for npm)

## Development

### Project Structure
```
CFG QODER/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── cfg_parser.py       # CFG parser implementation
│   ├── models.py           # Database models
│   ├── config.py           # Configuration
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   ├── utils/          # Utility functions
│   │   └── types/          # TypeScript types
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
└── README.md
```

### Available Scripts

#### Backend
- `py app.py` - Start development server
- `py -m pytest` - Run tests (if test files exist)

#### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Production Deployment

### Backend Deployment
1. Set environment variables:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url
```

2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn app:app
```

### Frontend Deployment
1. Build the production version:
```bash
npm run build
```

2. Deploy the `dist/` folder to your web server or hosting platform

### Environment Variables

#### Backend (.env)
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///cfg_validator.db
CORS_ORIGINS=https://your-frontend-domain.com
```

#### Frontend (.env)
```
VITE_API_URL=https://your-backend-domain.com/api
```

## Features Overview

### 🔍 **Real-time Validation**
- Instant HTTP request validation
- Detailed error messages
- Parse tree visualization

### 📊 **Analytics Dashboard**
- Validation statistics
- Error pattern analysis
- Success rate tracking

### 📚 **Learning Resources**
- Interactive grammar explorer
- Example request library
- Error explanation system

### 🤖 **AI Assistant**
- Context-aware help system
- CFG rule explanations
- HTTP syntax guidance

### 🎨 **Professional Design**
- Responsive layout
- Clean typography
- Accessible color scheme

## Support

If you encounter any issues:

1. Check this setup guide
2. Review the console logs for error messages
3. Ensure all dependencies are properly installed
4. Verify that both backend and frontend servers are running

## Technical Details

- **Frontend**: React 18 + TypeScript + TailwindCSS + Vite
- **Backend**: Python 3 + Flask + SQLAlchemy + NLTK
- **Database**: SQLite (development) / PostgreSQL (production)
- **Charts**: Recharts + D3.js
- **Validation**: NLTK Context-Free Grammar parser

## License

MIT License - see LICENSE file for details.