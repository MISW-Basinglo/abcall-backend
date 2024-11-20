import json
import unittest
from unittest.mock import patch, MagicMock
from src.services.gemini import GeminiAI


class TestGeminiAI(unittest.TestCase):
    @patch("src.services.gemini.genai.GenerativeModel")
    def test_config_model_generative(self, mock_generative_model):
        # Mock del modelo generado por genai
        mock_model_instance = MagicMock()
        mock_generative_model.return_value = mock_model_instance

        # Crear una instancia de GeminiAI generative (esto ya llama a config_model)
        gemini_ai = GeminiAI(kind="generative")

        # Verificar que el modelo se configuró correctamente
        mock_generative_model.assert_called_once_with(
            model_name="gemini-1.5-pro",
            safety_settings=gemini_ai.safety_settings,
            generation_config=gemini_ai.generation_config,
            system_instruction=gemini_ai.get_instruction(),
        )

    def test_get_instruction_generative(self):
        # Crear una instancia de GeminiAI generative
        gemini_ai = GeminiAI(kind="generative")
        instruction = gemini_ai.get_instruction()

        # Verificar que se devuelva la instrucción generativa base
        self.assertIn("Eres un gestor de call center experto", instruction)
        self.assertNotIn("Actúa como un experto en análisis", instruction)

    def test_get_instruction_predictive(self):
        # Crear una instancia de GeminiAI predictive
        gemini_ai = GeminiAI(kind="predictive")
        instruction = gemini_ai.get_instruction()

        # Verificar que se devuelva la instrucción predictiva base
        self.assertIn("Actúa como un experto en análisis de incidentes", instruction)
        self.assertNotIn("Eres un gestor de call center experto", instruction)

    def test_get_instruction_predictive_with_data(self):
        # Crear una instancia de GeminiAI predictive con datos adicionales
        gemini_ai = GeminiAI(kind="predictive")
        data = {"incidents": [{"id": 1, "description": "Issue 1"}]}
        instruction = gemini_ai.get_instruction(data=data)

        # Verificar que la instrucción incluye los datos adicionales
        self.assertIn("Actúa como un experto en análisis de incidentes", instruction)
        self.assertIn(json.dumps(data, indent=4), instruction)

    def test_invalid_kind(self):
        # Intentar crear una instancia con un tipo inválido
        with self.assertRaises(ValueError) as context:
            GeminiAI(kind="invalid")
        self.assertEqual(str(context.exception), "Invalid kind: invalid")


if __name__ == "__main__":
    unittest.main()
