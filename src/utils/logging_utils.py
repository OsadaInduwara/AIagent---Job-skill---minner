import logging
import sys
from datetime import datetime


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger("ai_job_skills_platform")


def get_logger(name: str):
    return logging.getLogger(f"ai_job_skills_platform.{name}")