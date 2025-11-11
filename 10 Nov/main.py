# Backend
import os
import logging
import time
from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# ---------------- Logging ----------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/StreamlitWithFastAPI.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct:free",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)


app = FastAPI()

class Query(BaseModel):
    text: str

# ---------------- API Middleware ----------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"API call: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"API call completed in {duration:.4f} seconds")
    return response

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

@app.post("/process/")
def process_input(query: Query):
    text = query.text.lower().strip()

    # Logic for different types of queries
    if "add" in text:
        # Example: "add 45 and 35"
        numbers = [int(word) for word in text.split() if word.isdigit()]
        if len(numbers) == 2:
            result = numbers[0] + numbers[1]
            return {"answer": f"The sum is {result}"}

    elif "date" in text:
        today = datetime.now().strftime("%Y-%m-%d")
        return {"answer": f"Today's date is {today}"}

    elif "reverse" in text:
        # Example: "reverse this word: Abdullah"
        word = text.split(":")[-1].strip()
        return {"answer": f"Reversed: {word[::-1]}"}

    else:
        try:
            messages = [
                SystemMessage(content="You are a helpful and concise AI assistant."),
                HumanMessage(content=text)
            ]
            response = llm.invoke(messages)

            return {"answer": response.content.strip() if response.content else "(no response)"}

        except Exception as e:
            return {"answer": f"Error: {e}"}

