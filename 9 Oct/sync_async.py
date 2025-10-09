from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# --------------------------- SYNC ENDPOINT ------------------------
@app.get("/sync-tasks")
def sync_tasks():
    time.sleep(10)
    return {"message": "Sync task completed after 10 seconds"}

# --------------------------- ASYNC ENDPOINT -----------------------
@app.get("/async-tasks")
async def async_tasks():
    await asyncio.sleep(10)
    return {"message": "Async task completed after 5 seconds"}