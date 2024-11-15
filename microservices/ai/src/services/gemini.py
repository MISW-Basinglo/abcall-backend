import json

import google.generativeai as genai
from src.services.base import BaseAI


class GeminiAI(BaseAI):
    BASE_GENERATIVE_INSTRUCTION = """
        Eres un gestor de call center experto en resolver problemas e incidencias de los clientes.
        Tu tarea es proporcionar soluciones precisas y efectivas a las consultas de los usuarios.
        Analiza cada situación con detenimiento y ofrece respuestas que aborden directamente los problemas planteados.
        Prioriza la claridad y la eficiencia en tus explicaciones, asegurándote de que el usuario entienda la solución propuesta.
        Si las opciones de solución que ofreces no funcionan, indica al usuario que debe crear una incidencia en el sistema
        y que se le contactará a la mayor brevedad posible.
        No es necesario presentarse ni realizar formalidades, solo enfócate en ofrecer la respuesta más certera posible.
        No des respuestas como si estuvieras hablando con alguien, solamente enfócate en los pasos para intentar resolver el problema.
    """

    BASE_PREDICTIVE_INSTRUCTION = """
        Eres un experto en análisis de datos y predicción de tendencias.
        Tu tarea es con base a una entrada de todos los incidentes registrados en el sistema, y con un identificador único llamado "incident_id",
        revisas incidentes similares y sugieres tres alternativas de solución al id del incidente enviado.
        Si el id del incidente no se encuentra en el sistema, debes indicar que no se encontró información.
    """

    def __init__(self, model_name="gemini-1.5-pro", kind="generative", **kwargs):
        self.kind = kind
        super().__init__(model_name, **kwargs)

    def config_model(self, model_name="gemini-1.5-pro"):
        return genai.GenerativeModel(
            model_name=model_name,
            safety_settings=self.safety_settings,
            generation_config=self.generation_config,
            system_instruction=self.get_instruction(),
        )

    def get_instruction(self, **kwargs):
        if self.kind == "generative":
            return self.BASE_GENERATIVE_INSTRUCTION
        elif self.kind == "predictive":
            instruction = self.BASE_PREDICTIVE_INSTRUCTION
            if "data" in kwargs:
                instruction += "\n\n" + json.dumps(kwargs["data"], indent=4)
            return instruction
        else:
            raise ValueError(f"Invalid kind: {self.kind}")
