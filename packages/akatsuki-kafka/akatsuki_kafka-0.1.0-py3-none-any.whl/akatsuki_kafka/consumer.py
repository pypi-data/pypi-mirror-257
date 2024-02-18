from aiokafka import AIOKafkaConsumer, ConsumerRecord

from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from google.protobuf.message import Message

import asyncio
import signal
import logging

logger = logging.getLogger(__name__)

MessageT = TypeVar("MessageT", bound=Message)

class KafkaConsumer(Generic[MessageT]):
    def __init__(
        self,
        topic: str,
        bootstrap_servers: list[str],
        group_id: str,
    ) -> None:
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id

        self._consumer: AIOKafkaConsumer | None = None

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
            logger.info("Starting consumer")
            assert self._consumer is None
            self._consumer = AIOKafkaConsumer(
                self.topic,
                bootstrap_servers=",".join(self.bootstrap_servers),
                group_id=self.group_id,
                auto_offset_reset="earliest",
            )
            await self._consumer.start()
            logger.info("Started consumer")

        await self._consume()

    async def stop(self, reason: str | None = None) -> None:
        assert self._consumer is not None

        logger.info("Stopping consumer", extra={"reason": reason})
        await self._consumer.stop()
        logger.info("Stopped consumer")

        self.should_shutdown = True

    async def _handle_message(self, message: ConsumerRecord) -> None:
        assert message.value is not None
        parsed_message = self.parse_message(message.value)

        await self.handle_message(parsed_message)

    async def _consume(self) -> None:
        assert self._consumer is not None

        while not self.should_shutdown:
            async for message in self._consumer:
                await self._handle_message(message)

    @abstractmethod
    def parse_message(self, message: bytes) -> MessageT:
        ...

    @abstractmethod
    async def handle_message(self, message: MessageT) -> None:
        ...