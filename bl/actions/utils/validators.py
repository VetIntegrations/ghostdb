import typing

from ghostdb import exceptions


class ValidationError(exceptions.GhostDBException):
    message = 'Not Valid'


class RequiredFields:

    def __init__(self, fields: typing.Tuple[str]):
        self.fields = fields

    def __call__(self, obj) -> bool:
        empty_fields = [
            field
            for field in self.fields
            if getattr(obj, field) is None
        ]
        if empty_fields:
            raise ValidationError(
                'Empty required fields: {}'.format(', '.join(empty_fields))
            )

        return True
