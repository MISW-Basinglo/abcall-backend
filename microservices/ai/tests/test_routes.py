import unittest
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from src.routes import blueprint  # Asegúrate de cambiar esto por la ruta correcta
from unittest.mock import patch


class TestAIBlueprint(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Configuración de la app Flask para pruebas
        cls.app = Flask(__name__)
        cls.app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Cambia por una clave segura
        cls.jwt = JWTManager(cls.app)
        cls.app.register_blueprint(blueprint)

    def setUp(self):
        # Crear un cliente de prueba para realizar peticiones
        self.client = self.app.test_client()

    def test_health_get(self):
        # Realizar la solicitud GET al endpoint /health
        response = self.client.get('/ai/health')
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
