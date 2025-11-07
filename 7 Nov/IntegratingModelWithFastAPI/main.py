from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, constr
from dotenv import load_dotenv
import os, json, requests, re
from datetime import datetime

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------- Data Model ----------
class Prompt(BaseModel):
    topic: constr(strip_whitespace=True, min_length=1)
    question: constr(strip_whitespace=True, min_length=1)

# ---------- Constants ----------
HISTORY_FILE = "qa-history.json"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json"
}

# ---------- Helper: Clean unwanted symbols ----------
def clean_text(text: str) -> str:
    # Remove unwanted markdown symbols
    text = re.sub(r"[*_#>`~]", "", text)

    # Add line breaks before numbered list items (e.g., "1.", "2.")
    text = re.sub(r"(\d+\.)", r"\n\1", text)

    # Add line breaks before bullet points or similar list indicators
    text = re.sub(r"([•\-–])", r"\n\1", text)

    # Replace multiple spaces or newlines with a single space/newline
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


# ---------- API Endpoint ----------
@app.post("/generate")
async def generate_response(prompt: Prompt):
    payload = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",
        "messages": [
            {"role": "system", "content": f"You are a helpful AI tutor for {prompt.topic}."},
            {"role": "user", "content": prompt.question}
        ]
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        cleaned_answer = clean_text(answer)

        # Save to history
        entry = {
            "timestamp": datetime.now().isoformat(),
            "topic": prompt.topic,
            "question": prompt.question,
            "answer": cleaned_answer
        }

        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w") as f:
                json.dump([entry], f, indent=2)
        else:
            with open(HISTORY_FILE, "r+") as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)

        return {"response": cleaned_answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------- Serve Frontend ----------
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")
