from abc import ABC
from abc import abstractmethod


class BaseAI(ABC):
    def __init__(self, model_name, **kwargs):
        self.model = self.config_model(model_name, **kwargs)

    @property
    def safety_settings(self):
        return [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]

    @property
    def generation_config(self):
        return {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

    @abstractmethod
    def get_instruction(self, **kwargs):
        pass

    @abstractmethod
    def config_model(self, model_name):
        pass
