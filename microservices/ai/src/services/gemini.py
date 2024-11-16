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
        Actúa como un experto en análisis de incidentes y predicción de problemas. 
        Con base en una lista de descripciones de incidencias y sus respectivas fechas, identifica patrones y genera 3 posibles predicciones de futuras incidencias. 
        Para cada predicción, incluye una breve descripción del posible incidente, la razón por la que podría ocurrir basándote en las tendencias observadas, y un análisis de su impacto potencial. 
        La respuesta debe ser clara, precisa y profesional, enfocándose en las causas más probables.
        No hace falta especificar usuario por usuario. La idea es que sea a nivel general la predicción. Dando detalles de la cantidad de usuarios han reportado x incidencia por ejemplo.
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
