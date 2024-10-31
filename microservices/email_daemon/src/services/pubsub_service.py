import json

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1
from src.common.constants import GOOGLE_CLOUD_PROJECT
from src.common.constants import PUBSUB_TOPIC
from src.common.logger import logger


class PubSubService:
    project_id = GOOGLE_CLOUD_PROJECT
    topic_id = PUBSUB_TOPIC

    def __init__(self, publisher=None):
        self.publisher = publisher or pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)
        self._create_topic_if_not_exists()

    def _create_topic_if_not_exists(self):
        """
        Creates the topic if it does not already exist.
        """
        try:
            self.publisher.create_topic(request={"name": self.topic_path})
            logger.info(f"Topic {self.topic_id} created.")
        except AlreadyExists:
            logger.info(f"Topic {self.topic_id} already exists.")

    def publish_message(self, data: dict) -> str:
        """
        Publishes a message to the topic.

        :param data: The data to publish, provided as a dictionary.
        :return: The message ID of the published message.
        """
        # Serialize data to JSON and encode as bytes
        message_data = json.dumps(data, ensure_ascii=False).encode("utf-8")

        # Publish message to the topic
        future = self.publisher.publish(self.topic_path, message_data)
        message_id = future.result()

        logger.info(f"Published message to {self.topic_id}: {message_id}")
        return message_id
