import asyncio
from ..config import get_settings


class QueueManager:
    _instance = None
    _semaphore = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self):
        if not self._initialized:
            settings = get_settings()
            self._semaphore = asyncio.Semaphore(settings.queue_max_connections)
            self._initialized = True

    async def acquire(self):
        if self._semaphore is None:
            self.initialize()
        await self._semaphore.acquire()

    def release(self):
        if self._semaphore is not None:
            self._semaphore.release()

    @property
    def max_connections(self) -> int:
        settings = get_settings()
        return settings.queue_max_connections


queue_manager = QueueManager()
