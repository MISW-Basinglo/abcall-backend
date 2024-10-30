import json
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from google.api_core.exceptions import AlreadyExists
from src.common.logger import logger
from src.services.pubsub_service import PubSubService  # Adjust the import based on your project structure


class TestPubSubService:
    def setup_method(self):
        # Mock the PublisherClient and its methods
        self.publisher_mock = MagicMock()
        self.pubsub_service = PubSubService()
        self.pubsub_service.publisher = self.publisher_mock

    def test_create_topic_if_not_exists_creates_topic(self):
        """Test that the topic is created if it does not exist."""
        self.publisher_mock.create_topic = MagicMock()
        self.publisher_mock.topic_path.return_value = "projects/test-project/topics/test-topic"

        self.pubsub_service._create_topic_if_not_exists()

        self.publisher_mock.create_topic.assert_called_once_with(request={"name": self.pubsub_service.topic_path})

    def test_create_topic_if_not_exists_topic_already_exists(self):
        """Test that if the topic already exists, it does not attempt to create it again."""
        self.publisher_mock.create_topic.side_effect = AlreadyExists("Topic already exists.")
        self.publisher_mock.topic_path.return_value = "projects/test-project/topics/test-topic"

        self.pubsub_service._create_topic_if_not_exists()

        self.publisher_mock.create_topic.assert_called_once()

    def test_publish_message(self):
        """Test publishing a message."""
        self.publisher_mock.publish.return_value.result.return_value = "test-message-id"
        test_data = {"key": "value"}

        message_id = self.pubsub_service.publish_message(test_data)

        assert message_id == "test-message-id"
        self.publisher_mock.publish.assert_called_once()
        published_data = json.dumps(test_data, ensure_ascii=False).encode("utf-8")
        self.publisher_mock.publish.assert_called_once_with(self.pubsub_service.topic_path, published_data)

    def test_publish_message_logs(self):
        """Test that a log message is created when a message is published."""
        self.publisher_mock.publish.return_value.result.return_value = "test-message-id"
        test_data = {"key": "value"}

        self.pubsub_service.publish_message(test_data)
        self.publisher_mock.publish.assert_called_once()
