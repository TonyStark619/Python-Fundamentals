# Phase 2, Day 32: Enterprise Model Deployment (REST API)
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

print("--- Booting AI Server Infrastructure ---")

# 1. Initialize the Web Server
app = FastAPI(title="Placement AI Engine", version="1.0")

# 2. Define the exact JSON structure we expect from the frontend
class UserQuery(BaseModel):
    user_id: str
    prompt: str

# 3. Simulate our loaded AI Model (e.g., The RAG pipeline you built yesterday)
def generate_ai_response(text: str) -> str:
    # In a real production file, this passes the text into your PyTorch/Transformer model
    if "SAP" in text.upper():
        return "Target dynamic programming, trees, and system design for SAP."
    elif "TCS" in text.upper():
        return "Focus heavily on string manipulation, arrays, and numerical aptitude for TCS."
    else:
        return "Analyze the problem statement carefully and optimize for O(N) time complexity."

# 4. Create the API Endpoint (The bridge to the outside world)
@app.post("/api/v1/predict")
async def get_prediction(query: UserQuery):
    print(f"\n[SERVER LOG] Incoming request from User: {query.user_id}")
    print(f"[SERVER LOG] Payload: '{query.prompt}'")
    
    # Process the request through the AI
    answer = generate_ai_response(query.prompt)
    
    # Return standard JSON format to the client
    return {
        "status": "success",
        "model_used": "Custom-RAG-v1",
        "response": answer
    }

# 5. Boot the Server
if __name__ == "__main__":
    print("Status: FastAPI Server initialized. Waiting for incoming HTTP connections...")
    # This runs the server on localhost port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)