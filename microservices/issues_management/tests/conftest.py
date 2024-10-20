from datetime import timedelta
from unittest.mock import Mock

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
from src.repositories.base import BaseRepository

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
    app.config["JWT_SECRET_KEY"] = "your_secret_key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=30)
    app.config["TESTING"] = True
    with app.app_context():
        yield app


@pytest.fixture
def mock_session(mocker):
    """Fixture to create a mock database session."""
    return mocker.MagicMock()


@pytest.fixture
def mock_issue(mocker):
    """Fixture to create a mock issue."""
    return mocker.MagicMock()


@pytest.fixture
def mock_repository():
    class MockRepository(BaseRepository):
        model = Mock()
        serializer = Mock()
        model.__name__ = "MockModel"

    return MockRepository()


@pytest.fixture
def mock_get_auth_header(mocker):
    """Fixture to mock the get_auth_header_from_request function."""
    return mocker.patch("src.common.utils.get_auth_header_from_request")


@pytest.fixture
def mock_send_request(mocker):
    """Fixture to mock the send_request function."""
    return mocker.patch("src.common.utils.send_request")


@pytest.fixture
def mock_issue_repository(mocker):
    """Fixture to mock IssuesManagementRepository."""
    mock_repo = mocker.patch("src.repositories.issues_repository.IssuesManagementRepository")
    return mock_repo
