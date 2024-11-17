import json
import unittest
from unittest.mock import patch, MagicMock
from src.services.services import (
    get_generative_data,
    get_predictive_data,
    generative_chat_session,
    predictive_chat_session,
)
from src.common.utils import get_url, send_request
from src.entities import AIResponse
from src.serializers import GenericResponseSerializer
from flask import Flask

app = Flask(__name__)


class TestAIService(unittest.TestCase):

    @patch.object(generative_chat_session, "send_message")
    @patch("src.services.services.GenericResponseSerializer.dump")
    def test_get_generative_data(self, mock_dump, mock_send_message):
        # Simular el mensaje enviado y la respuesta del modelo
        mock_send_message.return_value = MagicMock(text="Respuesta generativa")
        mock_dump.return_value = {"text": "Respuesta generativa"}

        # Datos de entrada simulados
        data = {"msg": "¿Cuál es el estado de mi pedido?"}

        # Llamar a la función
        result = get_generative_data(data)

        # Verificaciones
        mock_send_message.assert_called_once_with(data["msg"])
        mock_dump.assert_called_once_with(AIResponse(text="Respuesta generativa"))
        self.assertEqual(result, {"text": "Respuesta generativa"})


if __name__ == "__main__":
    unittest.main()