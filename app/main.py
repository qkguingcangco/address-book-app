from fastapi import FastAPI
from .routers import address
from .logging_config import setup_logging
import logging

# logger
setup_logging()
logger = logging.getLogger(__name__)

try:
    app = FastAPI()
    app.include_router(address.router)
    logger.info("App has started")

except Exception as e:
    logger.error("Error encountered: %s", str(e))

