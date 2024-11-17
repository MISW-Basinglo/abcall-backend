import unittest
from unittest.mock import MagicMock, patch
from src.services.base import BaseAI


class TestBaseAI(unittest.TestCase):
    def setUp(self):
        # Crear una clase hija simulada para testear la funcionalidad abstracta
        class MockAI(BaseAI):
            def get_instruction(self, **kwargs):
                return "Mock instruction"

            def config_model(self, model_name, **kwargs):
                return {"model_name": model_name, **kwargs}

        self.MockAI = MockAI

    def test_safety_settings(self):
        mock_ai = self.MockAI(model_name="test-model")
        expected_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        self.assertEqual(mock_ai.safety_settings, expected_settings)

    def test_generation_config(self):
        mock_ai = self.MockAI(model_name="test-model")
        expected_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.assertEqual(mock_ai.generation_config, expected_config)

    def test_get_instruction(self):
        mock_ai = self.MockAI(model_name="test-model")
        self.assertEqual(mock_ai.get_instruction(), "Mock instruction")

    def test_abstract_methods(self):
        # Probar que la clase BaseAI no puede ser instanciada directamente
        with self.assertRaises(TypeError):
            BaseAI(model_name="test-model")


if __name__ == "__main__":
    unittest.main()
