# Technology Stack

## Programming Language
- **Python**: Primary language for all components
- **Version**: Compatible with Python 3.8+

## Core Frameworks & Libraries

### Web Frameworks
- **FastAPI 0.109.0**: Modern, high-performance REST API framework
  - Automatic API documentation (Swagger/OpenAPI)
  - Built-in request validation with Pydantic
  - Async support for improved performance
  
- **Uvicorn 0.27.0**: ASGI server for running FastAPI
  - Production-ready web server
  - Hot reload support for development

- **Streamlit 1.31.0**: Interactive web application framework
  - Rapid UI development for data applications
  - Built-in widgets and components
  - Real-time updates and interactivity

### AI & Machine Learning
- **OpenAI >= 1.30.0**: GPT model integration
  - Text summarization capabilities
  - Natural language understanding
  - Structured data extraction

### Utilities
- **python-dotenv 1.0.1**: Environment variable management
  - Loads configuration from `.env` files
  - Separates secrets from code

- **requests 2.31.0**: HTTP client library
  - Communication between Streamlit app and API server
  - Simple, elegant HTTP requests

## Database
- **PostgreSQL**: Optional relational database
  - Stores analysis history
  - Configurable based on deployment needs
  - Connection details managed via environment variables

## Development Setup

### Installation
```bash
pip install -r requirements.txt
```

### Environment Configuration
1. Create `.env` file from `.env.example`
2. Configure required variables:
   - `OPENAI_API_KEY`: OpenAI API authentication
   - PostgreSQL credentials (if using database)

### Database Initialization (Optional)
```bash
python db.py
```

## Development Commands

### Start API Server
```bash
uvicorn api:app --reload --port 8000
```
- `--reload`: Auto-restart on code changes (development mode)
- `--port 8000`: API accessible at http://localhost:8000

### Start Streamlit App
```bash
streamlit run app.py
```
- Default port: 8501
- Web interface at http://localhost:8501

### Running Both Services
Requires two terminal sessions:
1. Terminal 1: Start API server
2. Terminal 2: Start Streamlit app

## API Documentation
- **Swagger UI**: http://localhost:8000/docs (when API server running)
- **ReDoc**: http://localhost:8000/redoc (alternative documentation)

## Dependency Management
- **requirements.txt**: Pinned versions for reproducible builds
- All dependencies specified with exact or minimum versions
- No development/production split (single requirements file)

## Architecture Style
- **ASGI**: Asynchronous Server Gateway Interface for FastAPI
- **REST**: RESTful API design for HTTP endpoints
- **Client-Server**: Separation between UI and API layers
