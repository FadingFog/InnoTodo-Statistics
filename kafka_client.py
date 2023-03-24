import asyncio
import json
from typing import Callable

from aiokafka import AIOKafkaConsumer
from bson import json_util
from loguru import logger

from app.config import settings
from app.db import init_database
from app.models import UserAction
from app.services import StatisticsServices


class KafkaClient:
    def __init__(self, kafka_topic: str, kafka_bootstrap_servers: str, processing_func: Callable):
        self.kafka_topic = kafka_topic
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.consumer = None

        self._processing_func = processing_func

    async def consume(self):
        self.consumer = AIOKafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=self.kafka_bootstrap_servers,
        )

        try:
            await self.consumer.start()
            logger.info("Established Kafka connection")

            async for message in self.consumer:
                logger.debug("Consumed message: " + str(message))
                await self._processing_func(message)
        finally:
            await self.consumer.stop()


class MessageProcessing:
    @staticmethod
    async def init_database():
        await init_database()

    @staticmethod
    async def process_message(message):
        data = json.loads(message.value, object_hook=json_util.object_hook)
        action_schema = UserAction(**data)
        await StatisticsServices.create_user_action(action_schema)
        logger.debug("Message has been processed")


if __name__ == '__main__':
    try:
        kafka_client = KafkaClient(
            settings.KAFKA_TOPIC, settings.KAFKA_BOOTSTRAP_SERVERS, MessageProcessing.process_message
        )
        loop = asyncio.new_event_loop()
        loop.run_until_complete(MessageProcessing.init_database())
        loop.run_until_complete(kafka_client.consume())
    except Exception as exc:
        logger.exception(exc)
