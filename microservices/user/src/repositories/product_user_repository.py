from src.common.enums import AllowedRoles
from src.common.utils import get_request_url
from src.common.utils import send_request
from src.models.product_user import ProductUser
from src.repositories.base import BaseRepository


class ProductUserRepository(BaseRepository):
    model = ProductUser

    def __init__(self):
        super().__init__()