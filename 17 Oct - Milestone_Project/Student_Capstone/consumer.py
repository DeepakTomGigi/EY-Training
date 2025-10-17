import pika
import pandas as pd
import os
import time
import logging

# ---------------- Logging Setup ----------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------- RabbitMQ Consumer ----------------
def start_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='csv_queue')
        logger.info("RabbitMQ consumer started, waiting for CSVs...")
    except Exception as e:
        logger.error(f"Error connecting to RabbitMQ: {e}")
        return

    def callback(ch, method, properties, body):
        csv_file = body.decode()
        logger.info(f"[Queue] Received CSV: {csv_file}")

        # ---------------- ETL ----------------
        start_time = time.time()
        try:
            df = pd.read_csv(csv_file)
            logger.info(f"[ETL] Loaded CSV ({len(df)} rows)")
        except Exception as e:
            logger.error(f"[ETL] Error reading file {csv_file}: {e}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        try:
            df['TotalMarks'] = df['Maths'] + df['Python'] + df['ML']
            df['Percentage'] = (df['TotalMarks'] / 300) * 100
            df['Result'] = df['Percentage'].apply(lambda x: 'Pass' if x >= 50 else 'Fail')
            os.makedirs("processed", exist_ok=True)
            output_file = os.path.join("processed", f"results_{int(time.time())}.csv")
            df.to_csv(output_file, index=False)
            duration = time.time() - start_time
            logger.info(f"[ETL] Completed CSV {csv_file} in {duration:.2f}s, saved to {output_file}")
        except Exception as e:
            logger.error(f"[ETL] Processing error for {csv_file}: {e}")

        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"[Queue] Finished processing {csv_file}")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='csv_queue', on_message_callback=callback)
    channel.start_consuming()

# ---------------- Run Consumer ----------------
if __name__ == "__main__":
    start_consumer()
