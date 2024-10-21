from datetime import timezone

from sqlalchemy import DateTime


def set_utc_timestamps(mapper, connection, target):
    """
    This function will go through all columns in a model and ensure that any DateTime
    columns are converted to UTC.
    """
    for attr in target.__mapper__.columns:
        if isinstance(attr.type, DateTime) and attr.name in target.__dict__:
            value = getattr(target, attr.name)
            if value is not None:
                if value.tzinfo is None:
                    utc_value = value.replace(tzinfo=timezone.utc)
                else:
                    utc_value = value.astimezone(timezone.utc)

                setattr(target, attr.name, utc_value)
