import pika

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='csv_queue')

# CSV files to send
csv_file = "data/marks.csv"  # Add more CSV paths if needed

channel.basic_publish(
    exchange='',
    routing_key='csv_queue',
    body=csv_file
)
print(f"[Producer] Sent '{csv_file}' to queue")

connection.close()
