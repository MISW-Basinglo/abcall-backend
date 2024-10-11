from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from src.common.constants import DATABASE_URI
from src.events import set_utc_timestamps

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@event.listens_for(Base, "before_insert")
@event.listens_for(Base, "before_update")
def receive_before_insert_update(mapper, connection, target):
    set_utc_timestamps(mapper, connection, target)
