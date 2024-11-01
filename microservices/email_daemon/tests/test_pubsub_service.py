from unittest.mock import MagicMock
from unittest.mock import patch

from faker import Faker
from src.services.pubsub_service import PubSubService

fake = Faker()


def test_create_topic_if_not_exists():
    fake_topic_path = "fake_topic_path"
    patch("src.services.pubsub_service.PubSubService.publisher.create_topic")
    mock_publisher = MagicMock()
    mock_publisher.topic_path.return_value = fake_topic_path
    pubsub_instance = PubSubService(publisher=mock_publisher)
    assert pubsub_instance.publisher == mock_publisher
    assert pubsub_instance.topic_path == fake_topic_path


def test_publish_message():
    future_mock = MagicMock()
    future_mock.result.return_value = fake.uuid4()
    patch("src.services.pubsub_service.PubSubService.publisher.create_topic")
    mock_publisher = MagicMock()
    mock_publisher.publish.return_value = future_mock
    pubsub_instance = PubSubService(publisher=mock_publisher)
    message_id = pubsub_instance.publish_message({"test": "data"})

    assert str(message_id) == str(future_mock.result())
