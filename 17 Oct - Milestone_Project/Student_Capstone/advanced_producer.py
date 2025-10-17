from fastapi import FastAPI, UploadFile, File, HTTPException
import pika, os, shutil, logging

app = FastAPI(title="Student Pipeline Producer")

# Logging setup
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/pipeline.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_marks")
async def upload_marks(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Uploaded file saved: {file_path}")

        # Send file path to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="csv_queue")
        channel.basic_publish(exchange="", routing_key="csv_queue", body=file_path)
        connection.close()

        logger.info(f"File {file_path} pushed to RabbitMQ queue")
        return {"message": f"File {file.filename} sent for processing"}
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
