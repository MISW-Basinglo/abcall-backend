from src.routes.company_routes import blueprint as company_blueprint
from src.routes.user_routes import blueprint as user_blueprint
from src.routes.product_routes import blueprint as product_blueprint

blueprints = [user_blueprint, company_blueprint, product_blueprint]
