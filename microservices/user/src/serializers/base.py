import typing

from marshmallow import Schema
from marshmallow import types
from marshmallow import ValidationError
from src.common.enums import ExceptionsMessages
from src.common.enums import MarshmallowCustomValidationMessages
from src.common.exceptions import InvalidParameterException
from src.common.logger import logger


class BaseSerializer(Schema):
    def handle_error(self, exc, data, **kwargs):
        custom_errors = {}
        for field, error_messages in exc.messages.items():
            logger.error(f"Error during serialization: {error_messages} {data}")
            custom_errors[field] = []
            for msg in error_messages:
                if "Missing data" in msg:
                    custom_errors[field].append(MarshmallowCustomValidationMessages.MISSING_DATA.value.format(field=field))
                elif "Not a valid" in msg:
                    custom_errors[field].append(MarshmallowCustomValidationMessages.INVALID_DATA.value.format(field=field))
                else:
                    custom_errors[field].append(MarshmallowCustomValidationMessages.GENERIC_ERROR.value.format(field=field))
        raise ValidationError(custom_errors)

    def load(
        self,
        data: typing.Union[
            typing.Mapping[str, typing.Any],
            typing.Iterable[typing.Mapping[str, typing.Any]],
        ],
        *,
        many: typing.Optional[bool] = None,
        partial: typing.Optional[typing.Union[bool, types.StrSequenceOrSet]] = None,
        unknown: typing.Optional[str] = None,
    ):
        try:
            return super().load(data, many=many, partial=partial, unknown=unknown)
        except ValidationError as e:
            msg = e.messages[next(iter(e.messages))][0]
            raise InvalidParameterException(msg)
