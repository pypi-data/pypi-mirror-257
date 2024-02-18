from aiokafka import AIOKafkaProducer

from google.protobuf.message import Message
from typing import Optional

import logging
import asyncio
import signal

logger = logging.getLogger(__name__)

class KafkaProducer:
    def __init__(self, bootstrap_servers: list[str]) -> None:
        self.bootstrap_servers = bootstrap_servers

        self._producer: Optional[AIOKafkaProducer] = None

        self._lock = asyncio.Lock()
        self.should_shutdown = False

    async def _handle_signal(self) -> None:
        async with self._lock:
            await self.stop()

    def _add_signal_handlers(self) -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGUSR1, signal.SIGUSR2):
            loop.add_signal_handler(sig=sig, callback=lambda: asyncio.create_task(self._handle_signal()))

    async def start(self) -> None:
        self._add_signal_handlers()

        async with self._lock:
            logger.info("Starting producer")
            assert self._producer is None
            self._producer = AIOKafkaProducer(
                bootstrap_servers=",".join(self.bootstrap_servers),
            )
            await self._producer.start()
            logger.info("Started producer")

    async def stop(self, reason: Optional[str] = None) -> None:
        assert self._producer is not None

        logger.info("Stopping producer", extra={"reason": reason})
        await self._producer.stop()
        logger.info("Stopped producer")

        self.should_shutdown = True

    async def publish(
        self,
        topic: str,
        partition_key: str,
        message: Message,
    ) -> None:
        assert self._producer is not None
        assert not self.should_shutdown

        await self._producer.send_and_wait(
            topic=topic,
            key=partition_key.encode("utf-8"),
            value=message.SerializeToString(),
        )
