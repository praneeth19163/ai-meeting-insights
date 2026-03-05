# Text Analysis Tool

A tool to summarize long texts and extract action items & key decisions using OpenAI GPT.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key and PostgreSQL credentials

3. **Setup database (optional):**
   ```bash
   python db.py
   ```

## Running the Application

1. **Start the API server:**
   ```bash
   uvicorn api:app --reload --port 8000
   ```

2. **Start the Streamlit app (in a new terminal):**
   ```bash
   streamlit run app.py
   ```

3. **Access the app:**
   - Open your browser to `http://localhost:8501`

## API Endpoints

- `POST /analyze-text` - Basic text analysis (length, word count)
- `POST /summarize` - Generate summary from long text
- `POST /extract` - Extract action items and key decisions from summary

## Architecture

**2-Call Approach:**
1. Long Text → `/summarize` → Summary
2. Summary → `/extract` → Action Items + Key Decisions

This approach balances accuracy, cost, and performance.
