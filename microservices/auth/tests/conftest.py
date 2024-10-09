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
from src.models.permission import Permission
from src.models.role import Role
from src.models.user import User

fake = Faker()
from src.db import Base


@pytest.fixture(scope="session")
def create_test_database():
    # The name of the test database
    test_db_name = f"{DATABASE_NAME}_test"

    # Connect to the default 'postgres' database to create the test database
    connection = psycopg2.connect(
        dbname="postgres",
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,  # You need to connect to an existing DB first, like 'postgres'
    )
    connection.autocommit = True
    cursor = connection.cursor()

    # Drop the test database if it exists, and create a new one
    cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name};")
    cursor.execute(f"CREATE DATABASE {test_db_name};")
    print("Database created!!")
    cursor.close()
    connection.close()

    # Yield to allow tests to run
    yield

    # Cleanup: drop the test database after tests
    connection = psycopg2.connect(
        dbname="postgres",
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,  # Connect to 'postgres' again to drop the test DB
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name};")
    cursor.close()
    connection.close()


@pytest.fixture(scope="session")
def engine(create_test_database):
    # Use the test database
    test_db_uri = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}_test"

    engine = create_engine(test_db_uri, echo=True)
    Base.metadata.create_all(engine)  # Create all tables

    yield engine

    engine.dispose()


@pytest.fixture(scope="function")
def session(engine):
    # Create a new connection and transaction
    connection = engine.connect()
    transaction = connection.begin()

    # Create a new session
    Session = sessionmaker(bind=connection)
    session = Session()

    # Yield the session to the test
    yield session

    # Rollback transaction and close session
    session.close()  # Close the session
    transaction.rollback()  # Rollback the transaction
    connection.close()  # Close the connection


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
    """Fixture to create a user role with some permissions."""
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
    """Fixture to create a user and associate roles."""
    user = User(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    password = fake.password()
    user.set_password(password)
    user.roles = [role_admin, role_user]
    session.add(user)
    session.commit()
    return user, password


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
    """Fixture to create a mock user."""
    user = mocker.MagicMock(spec=User)
    user.id = 1
    user.email = "test@example.com"
    user.check_password = mocker.Mock(return_value=True)
    return user


@pytest.fixture
def login_data():
    """Fixture to provide login data."""
    return {"email": "test@example.com", "password": "password123"}
