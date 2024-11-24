import json

from src.common.utils import get_url
from src.common.utils import send_request
from src.entities import AIResponse
from src.serializers import GenericResponseSerializer
from src.services.gemini import GeminiAI

generative_model = GeminiAI(kind="generative")
predictive_model = GeminiAI(kind="predictive")

generative_chat_session = generative_model.model.start_chat(history=[])

predictive_chat_session = predictive_model.model.start_chat(history=[])


def get_generative_data(data):
    response = generative_chat_session.send_message(data["msg"])
    response_entity = AIResponse(text=response.text)
    return GenericResponseSerializer().dump(response_entity)


def get_predictive_data(company_id: int):
    data = {}
    data["company_id"] = company_id
    url = get_url(path_name="issues", params=data)
    data = send_request("GET", url)
    response = predictive_chat_session.send_message(json.dumps(data))
    response_entity = AIResponse(text=response.text)
    return GenericResponseSerializer().dump(response_entity)
