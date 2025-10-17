import pika, pandas as pd, os, time, logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/pipeline.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

def start_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="csv_queue")
        logger.info("Consumer started, waiting for files...")
        print("[*] Consumer started, waiting for files...")

    except Exception as e:
        logger.error(f"RabbitMQ connection error: {e}")
        print(f"RabbitMQ connection error: {e}")
        return

    def callback(ch, method, properties, body):
        csv_file = body.decode()
        logger.info(f"[Queue] Received: {csv_file}")
        print(f"[Queue] Received: {csv_file}")

        try:
            df = pd.read_csv(csv_file)
            df["TotalMarks"] = df["Maths"] + df["Python"] + df["ML"]
            df["Percentage"] = (df["TotalMarks"] / 300) * 100
            df["Result"] = df["Percentage"].apply(lambda x: "Pass" if x >= 50 else "Fail")

            os.makedirs("data/processed/advanced_results", exist_ok=True)
            output_file = os.path.join("data/processed/advanced_results", f"results_{int(time.time())}.csv")
            df.to_csv(output_file, index=False)
            logger.info(f"[ETL] Processed file saved to {output_file}")
            print(f"[ETL] Processed file saved to {output_file}")
        except Exception as e:
            logger.error(f"[ETL] Error processing {csv_file}: {e}")
            print(f"[ETL] Error processing {csv_file}: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"[Queue] Completed {csv_file}")

    channel.basic_consume(queue="csv_queue", on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
