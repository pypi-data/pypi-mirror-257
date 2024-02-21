from typing import Callable

import uvicorn
from fastapi import FastAPI
from loguru import logger


class FastServer:
    def __init__(self, port):
        self.port = port
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("/probe")
        @self.app.post("/probe")
        async def probe():
            """Health check."""
            return {"status": "OK"}

        @self.app.post("/start")
        @self.app.get("/start")
        async def start(message):
            return {"message": message}

    def run(self, callback: Callable = None):
        logger.info(f"HTTP_SERVICE LISTEN: `0.0.0.0:{self.port}`")
        if callback:
            self._callback_func = callback
        uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info", log_config=None)
