import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Example logs
logging.debug("This is a debug message")
logging.info("Application started")
logging.warning("Low memory warning")
logging.error("File not found error")
logging.critical("Critical system failure")


