from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import InMemoryRunner
from dotenv import load_dotenv
import os

# Load env before importing agent
env_path = os.path.join(os.path.dirname(__file__), 'my_agent', '.env')
load_dotenv(env_path)

from my_agent.agent import root_agent
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gig Agent API")
runner = InMemoryRunner(agent=root_agent)

class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    response: str

@app.get("/")
def health_check():
    return {"status": "ok", "agent": "GigPlatformBrain"}

@app.post("/chat", response_model=QueryResponse)
async def chat_endpoint(request: QueryRequest):
    logger.info(f"Received Query: {request.text}")
    try:
        # run_debug returns List[Event]
        # We use a fixed session_id for now to keep context in this simple demo
        events = await runner.run_debug(request.text, session_id="demo_session", quiet=True)
        
        # Extract text from the last meaningful event
        # We iterate and concatenate 'text' attributes if they exist
        output_text = ""
        for event in events:
            # We look for simple text content in the events
            if hasattr(event, 'text') and event.text:
                # We might want only the final response, but let's grab all model output for now.
                # Heuristic: If it looks like a final answer.
                pass

        # Since parsing Event structure blindly is risky, let's rely on print output logic refactored
        # Or simpler: The last event usually contains the final response text in `content` or `text`.
        # Let's dump the last event to string if check fails.
        if events:
             # Basic heuristic: Search for the last event with 'text'
             for e in reversed(events):
                 if hasattr(e, 'text') and e.text:
                     output_text = e.text
                     break
                 if hasattr(e, 'content') and e.content:
                     # Check if content has 'parts' (common in ADK ModelResponse)
                     if hasattr(e.content, 'parts'):
                         parts_text = []
                         for part in e.content.parts:
                             if hasattr(part, 'text') and part.text:
                                 parts_text.append(part.text)
                         if parts_text:
                             output_text = "\n".join(parts_text)
                             break
                     # Fallback to direct text attribute or string conversion if 'parts' missing but not empty
                     elif hasattr(e.content, 'text') and e.content.text:
                         output_text = e.content.text
                         break
                     
                     # If we are here, it might be a weird object, but let's try not to return raw repr
                     # Only use str() as last resort if it looks like a string
                     if isinstance(e.content, str):
                        output_text = e.content
                        break
        
        if not output_text:
            output_text = "No response generated."

        return QueryResponse(response=output_text)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
