# Gig Worker's Intelligent Assistant 👷

A full-stack AI agent platform for connecting gig workers with jobs, featuring intelligent pricing and searching.

## Components
1.  *Backend API*: FastAPI (Agents, Logic, Data)
2.  *Frontend UI*: Streamlit (Chat Interface)

## Prerequisites
- Python 3.10+
- Google Cloud Project with Vertex AI API enabled (OR Google AI Studio Key)

## Setup
1.  *Clone/Open Folder*:
    bash
    cd /path/to/gig
    
2.  *Install Dependencies*:
    bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    # OR manually:
    pip install google-adk google-genai fastapi uvicorn streamlit python-dotenv
    
3.  *Configure Credentials*:
    - Ensure my_agent/.env exists with your GOOGLE_API_KEY.

## Running the Application (2 Terminal Windows)

### Terminal 1: Background Service (API)
Start the AI Agent backend.
bash
source venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 1234 --reload


### Terminal 2: Frontend (UI)
Start the Chat Interface.
bash
source venv/bin/activate
streamlit run app.py --server.port 1235


## Usage
- Open Browser to: http://localhost:1234
- Start chatting!