import logging
import os
from datetime import datetime

logfile = f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.log"

logfile_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logfile_path, exist_ok=True)

log_file = os.path.join(logfile_path, logfile)

logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    format="[%(asctime)s] %(lineno)d: %(name)s - %(levelname)s: %(message)s"
)