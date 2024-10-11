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
from src.models.auth import UserAuth
from src.models.permission import Permission
from src.models.role import Role

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


@pytest.fixture
def permission_read(session):
    """Fixture to create a permission."""
    permission = Permission(name="read")
    session.add(permission)
    session.commit()
    return permission


@pytest.fixture
def permission_write(session):
    """Fixture to create a permission."""
    permission = Permission(name="write")
    session.add(permission)
    session.commit()
    return permission


@pytest.fixture
def permission_delete(session):
    """Fixture to create a permission."""
    permission = Permission(name="delete")
    session.add(permission)
    session.commit()
    return permission


@pytest.fixture
def role_admin(session, permission_read, permission_write, permission_delete):
    """Fixture to create an admin role with some permissions."""
    permissions = [
        permission_read,
        permission_write,
        permission_delete,
    ]
    role = Role(name="admin")
    for perm in permissions:
        role.permissions.append(perm)
    session.add(role)
    session.commit()
    return role


@pytest.fixture
def role_user(session, permission_read):
    """Fixture to create a user_auth role with some permissions."""
    permissions = [
        permission_read,
    ]
    role = Role(name="user")
    for perm in permissions:
        role.permissions.append(perm)
    session.add(role)
    session.commit()
    return role


@pytest.fixture
def user_with_roles(session, role_admin, role_user):
    """Fixture to create a user_auth and associate roles."""
    user_auth = UserAuth(
        email=fake.email(),
    )
    password = fake.password()
    user_auth.set_password(password)
    user_auth.role = role_admin
    session.add(user_auth)
    session.commit()

    session.refresh(user_auth)

    return user_auth, password


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
def mock_user(mocker):
    """Fixture to create a mock user_auth."""
    user_auth = mocker.MagicMock(spec=UserAuth)
    user_auth.id = 1
    user_auth.email = "test@example.com"
    user_auth.check_password = mocker.Mock(return_value=True)
    return user_auth


@pytest.fixture
def login_data():
    """Fixture to provide login data."""
    return {"email": "test@example.com", "password": "password123"}
