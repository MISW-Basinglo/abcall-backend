import unittest
from src.entities import AIResponse  # Asegúrate de cambiar esto por la ruta correcta


class TestAIResponse(unittest.TestCase):

    def test_ai_response_creation(self):
        # Crear una instancia de AIResponse con datos válidos
        response = AIResponse(text="This is a test response")
        
        # Verificar que el valor del atributo 'text' sea correcto
        self.assertEqual(response.text, "This is a test response")

    def test_default_values(self):
        # Crear una instancia con valores predeterminados
        response = AIResponse(text="")
        
        # Verificar que el valor de 'text' sea el predeterminado
        self.assertEqual(response.text, "")

    def test_repr(self):
        # Verificar la representación de la instancia (output del __repr__)
        response = AIResponse(text="Test response")
        self.assertEqual(repr(response), "AIResponse(text='Test response')")


if __name__ == "__main__":
    unittest.main()
