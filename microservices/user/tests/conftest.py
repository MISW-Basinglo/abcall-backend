import psycopg2
import pytest
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.common.constants import DATABASE_HOST
from src.common.constants import DATABASE_NAME
from src.common.constants import DATABASE_PASSWORD
from src.common.constants import DATABASE_PORT
from src.common.constants import DATABASE_USER
from src.models.user import User
from src.models.company import Company
from datetime import datetime

fake = Faker()
from src.db import Base


@pytest.fixture(scope="session")
def create_test_database():
    test_db_name = f"{DATABASE_NAME}_test"

    connection = psycopg2.connect(
        dbname="postgres",
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
    )
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name};")
    cursor.execute(f"CREATE DATABASE {test_db_name};")
    cursor.close()
    connection.close()

    yield

    connection = psycopg2.connect(
        dbname="postgres",  # Connect to 'postgres' to drop the test DB
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name};")
    cursor.close()
    connection.close()


@pytest.fixture(scope="session")
def engine(create_test_database):
    test_db_uri = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}_test"

    engine = create_engine(test_db_uri, echo=True)
    Base.metadata.create_all(engine)

    yield engine

    engine.dispose()


@pytest.fixture(scope="function")
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    transaction.rollback()
    session.close()
    connection.close()


@pytest.fixture(scope="module")
def mock_app():
    from app import create_app

    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        yield app


@pytest.fixture
def mock_session(mocker):
    """Fixture to create a mock database session."""
    return mocker.MagicMock()


@pytest.fixture
def mock_company(mocker):
    """Fixture to create a mock company."""
    company = mocker.MagicMock(spec=Company)
    company.id = 1
    company.name = "Movistar"
    company.nit = "50912312"
    company.plan = "BUSINESS"
    company.status = "Active"
    company.created_at = datetime.now()
    company.update_at = datetime.now()
    return company


@pytest.fixture
def mock_company_data():
    """Fixture to provide mock company data."""
    return {
        "name": "Movistar",
        "nit": "50912312",
        "plan": "BUSINESS",
        "status": "Active"
    }


@pytest.fixture
def mock_user(mocker):
    """Fixture to create a mock user."""
    user = mocker.MagicMock(spec=User)
    user.id = 1
    user.name = "Test User"
    user.dni = "123456789"
    user.phone = "3102456789"
    user.channel = "EMAIL"
    user.auth_id = 2
    user.importance = 1
    user.company_id = 1  # Link to the mock company
    user.created_at = datetime.now()
    user.update_at = datetime.now()
    return user
