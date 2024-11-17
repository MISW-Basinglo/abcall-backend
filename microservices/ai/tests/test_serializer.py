import unittest
from marshmallow import ValidationError
from src.serializers import GenericResponseSerializer


class TestGenericResponseSerializer(unittest.TestCase):
    def setUp(self):
        self.serializer = GenericResponseSerializer()

    def test_valid_data(self):
        # Datos válidos
        valid_data = {"text": "This is a test message"}
        serialized = self.serializer.load(valid_data)
        self.assertEqual(serialized, valid_data)

    def test_invalid_text_field_type(self):
        # Tipo de dato inválido para 'text'
        invalid_data = {"text": 123}
        with self.assertRaises(ValidationError) as context:
            self.serializer.load(invalid_data)
        self.assertIn("Not a valid string.", str(context.exception))

    def test_dump_valid_data(self):
        # Serialización de datos válidos
        valid_data = {"text": "This is a test message"}
        dumped = self.serializer.dump(valid_data)
        self.assertEqual(dumped, valid_data)


if __name__ == "__main__":
    unittest.main()
