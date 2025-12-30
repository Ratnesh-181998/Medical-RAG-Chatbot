import logging
import os
from datetime import datetime, timedelta, timezone

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Define IST timezone (UTC + 5:30)
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_time():
    """Returns current time in IST"""
    return datetime.now(IST)

LOG_FILE = os.path.join(LOGS_DIR, f"log_{get_ist_time().strftime('%Y-%m-%d')}.log")

# Custom Formatter to enforce IST
class ISTFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.astimezone(IST)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s

# Configure Root Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File Handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(ISTFormatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S,%f'))
logger.addHandler(file_handler)

# Stream Handler (Optional: imports to console for debugging)
console_handler = logging.StreamHandler()
console_handler.setFormatter(ISTFormatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S,%f'))
logger.addHandler(console_handler)

def get_logger(name):
    return logging.getLogger(name)