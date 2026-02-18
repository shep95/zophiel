
import sys
import os

# Ensure the parent directory is in the path so we can import from Identity
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from Identity.god_mode import GodModeHunter

# Initialize FastAPI App
app = FastAPI(
    title="Zohar 'God Mode' Intelligence API",
    description="The All-Seeing Eye - Advanced OSINT Orchestration API",
    version="3.0.0"
)

# Enable CORS for Frontend Integration (Lovable.dev / React / Vue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize God Mode Hunter
hunter = GodModeHunter()

# --- Request Models ---
class InvestigationRequest(BaseModel):
    target_name: str
    location: Optional[str] = None
    dob: Optional[str] = None # YYYY-MM-DD
    address: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "online", "system": "Zohar God Mode Intelligence Node", "clearance": "LEVEL 5"}

@app.post("/api/v1/investigate")
def run_investigation(request: InvestigationRequest):
    """
    Triggers the GOD MODE Surveillance Protocol.
    1. Generates 50+ Username/Email Permutations
    2. Interrogates 40+ Social Networks
    3. Launches Zophiel Deep Web Engine
    4. Performs Recursive Spidering & Link Analysis
    """
    try:
        print(f"[API] GOD MODE ACTIVATED: {request.target_name}")
        
        # Execute the full directive
        report = hunter.execute_directive(
            name=request.target_name,
            dob=request.dob,
            location=request.location,
            address=request.address
        )
        
        return report

    except Exception as e:
        print(f"[API ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
