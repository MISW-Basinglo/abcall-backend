import json

from flask import current_app  # noqa
from src.common.logger import logger
from src.db import SessionLocal
from src.models.company import Company
from src.models.user import User
from src.models.product import Product
from src.models.product_user import ProductUser

FIXTURES_FILE_PATH = "src/fixtures/fixtures.json"  # Ruta de tu archivo JSON


def register_commands(app):
    @app.cli.command("load-fixtures")
    def load_fixtures():
        """Command to load test data (fixtures) from a JSON file."""
        logger.info(f"Loading test data from {FIXTURES_FILE_PATH}...")
        with open(FIXTURES_FILE_PATH, "r") as f:
            data = json.load(f)

        session = SessionLocal()

        # Cargar Compañías
        company_map = {}
        for company_data in data["companies"]:
            company = session.query(Company).filter_by(name=company_data["name"]).first()
            if not company:
                company = Company(name=company_data["name"], nit=company_data["nit"], plan=company_data["plan"], status=company_data["status"])
                session.add(company)
                logger.info(f"Added company: {company_data['name']}")
            company_map[company.name] = company

        session.flush()

        # Cargar Usuarios
        for user_data in data["users"]:
            user = session.query(User).filter_by(dni=user_data["dni"]).first()
            company = session.query(Company).filter_by(name=user_data["company_id"]).first()
            if not user:
                user = User(
                    name=user_data["name"],
                    dni=user_data["dni"],
                    phone=user_data["phone"],
                    channel=user_data["channel"],
                    auth_id=user_data["auth_id"],
                    importance=user_data["importance"],
                    company_id=company.id if company else None,
                )
                session.add(user)
                logger.info(f"Added user: {user_data['name']}")

        session.flush()

        # Cargar Productos
        for product_data in data["products"]:
            product = session.query(Product).filter_by(description=product_data["description"]).first()
            company = session.query(Company).filter_by(name=product_data["company_id"]).first()
            if not product:
                product = Product(
                    type=product_data["type"],
                    description=product_data["description"],
                    status=product_data["status"],
                    company_id=company.id if company else None,
                )
                session.add(product)
                logger.info(f"Added product: {product_data['description']}")
        
        session.flush()

        # Cargar Relacion Producto Usuario
        for product_users in data["product_user"]:
            product_id = product_users['product_id']
            product = session.query(Product).filter_by(id=product_id).first()
            user = session.query(User).filter_by(dni=product_users["id_user"]).first()
        
            product_user = ProductUser(
                id_user=user.id if user else None,
                product_id=product.id if product else None,
            )
            session.add(product_user)
            logger.info(f"Added product_user: {product_users['id_user']}")

        # Confirmar los cambios
        session.commit()
        session.close()
        logger.info(f"Test data loaded successfully from {FIXTURES_FILE_PATH}.")
