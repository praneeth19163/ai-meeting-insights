# Project Structure

## Directory Layout

```
python_task/
├── .amazonq/
│   └── rules/
│       └── memory-bank/          # Project documentation and guidelines
├── api.py                         # FastAPI REST API server
├── app.py                         # Streamlit web application
├── db.py                          # Database setup and management
├── README.md                      # Project documentation
└── requirements.txt               # Python dependencies
```

## Core Components

### api.py - REST API Server
**Purpose**: Provides HTTP endpoints for text analysis operations

**Responsibilities**:
- Exposes REST API endpoints for text analysis, summarization, and extraction
- Handles request validation and response formatting
- Integrates with OpenAI GPT models for AI processing
- Manages API server lifecycle using FastAPI framework

**Key Endpoints**:
- `/analyze-text` - Basic text statistics (length, word count)
- `/summarize` - Generate summaries from long text
- `/extract` - Extract action items and key decisions

### app.py - Web Interface
**Purpose**: Interactive user interface for text analysis

**Responsibilities**:
- Provides Streamlit-based web UI for manual text input
- Communicates with API server for processing
- Displays results in user-friendly format
- Handles user interactions and form submissions

**User Flow**:
1. User inputs long-form text via web form
2. App sends text to API endpoints
3. Results displayed with summaries and extracted items

### db.py - Database Management
**Purpose**: Optional data persistence layer

**Responsibilities**:
- PostgreSQL database schema setup
- Connection management
- Data storage for analysis history (optional feature)
- Database initialization and configuration

## Architectural Patterns

### Two-Tier Architecture
- **Backend Tier**: FastAPI server handling business logic and AI integration
- **Frontend Tier**: Streamlit app providing user interface

### Service-Oriented Design
- API server operates independently, enabling multiple client types
- Loose coupling between UI and processing logic
- RESTful communication pattern

### 2-Call Processing Pipeline
**Architecture Decision**: Balances accuracy, cost, and performance

```
Long Text → [Summarize] → Summary → [Extract] → Action Items + Key Decisions
```

**Rationale**:
- First call condenses information while preserving context
- Second call focuses on structured extraction from manageable text
- Reduces token usage compared to single-call approach
- Improves extraction accuracy by working with summarized content

## Component Relationships

```
User → app.py (Streamlit) → api.py (FastAPI) → OpenAI GPT
                                ↓
                            db.py (Optional)
```

### Data Flow
1. User submits text through Streamlit interface
2. Streamlit app makes HTTP requests to FastAPI server
3. FastAPI processes requests using OpenAI API
4. Results optionally stored in PostgreSQL database
5. Response returned to Streamlit for display

## Configuration Management
- Environment variables for API keys and database credentials
- `.env` file for local development configuration
- Separation of configuration from code
