from src.common.enums import AllowedRoles
from src.common.utils import get_request_url
from src.common.utils import send_request
from src.models.user import User
from src.repositories.base import BaseRepository
from src.serializers.user_serializers import UserRetrieveSerializer


class UserRepository(BaseRepository):
    model = User

    def __init__(self):
        super().__init__()

    def get_responsible_by_company(self, company_id: int):
        query_dict = {
            "company_id": ("eq", company_id),
            "importance": ("eq", None),
        }
        users = self.get_by_query(query_dict)
        responsible = None
        for user in users:
            auth_data = self.get_auth_user_data_service(user["auth_id"])
            if auth_data["role"] == AllowedRoles.CLIENT.value:
                user["email"] = auth_data["email"]
                responsible = user
                break
        if not responsible:
            raise Exception("No responsible found for company")
        return responsible

    @staticmethod
    def get_auth_user_data_service(auth_id: int):
        url = get_request_url("auth")
        auth_data = send_request("GET", f"{url}/{auth_id}")["data"]
        return UserRetrieveSerializer().load(auth_data)
