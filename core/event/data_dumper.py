import abc
import typing

from sqlalchemy import inspect
from sqlalchemy.orm.base import PASSIVE_OFF
from sqlalchemy.orm.state import InstanceState


class BaseDataDumper(abc.ABC):
    def __init__(self, obj):
        self.obj = obj

    @abc.abstractmethod
    def get_data_dump(self):
        ...


class GenericDataDumper(BaseDataDumper):

    def get_data_dump(self) -> dict:
        data_dump = self.get_modified_data()
        data_dump.update(self.get_pms_ids_data())
        return data_dump

    def get_modified_data(self) -> dict:
        data = dict()
        state = inspect(self.obj)
        modified_keys = self.get_modified_keys(state)
        for key in modified_keys:
            history = state.get_history(key, PASSIVE_OFF)
            data[key] = history.added[0]
        return data

    def get_pms_ids_data(self) -> dict:
        data = dict()
        pms_ids = getattr(self.obj, 'pms_ids', None)
        if pms_ids:
            data['pms_ids'] = pms_ids
        return data

    @staticmethod
    def get_modified_keys(state: InstanceState) -> set:
        keys = {attr.key for attr in state.attrs}
        unmodified_keys = state.unmodified
        return keys ^ unmodified_keys


class RelationDataDumper(GenericDataDumper):
    """Extend GenericDataDumper with ability to always get relation IDs

    How to use:
    from functools import partial

    xxxEvent(
        'name of event',
        data_dumper=partial(
            RelationDataDumper,
            pk_fields=('field1', 'field2', )
        )
    )
    """

    def __init__(self, obj, *, pk_fields: typing.Iterable[str]):
        super().__init__(obj)
        self.pk_fields = pk_fields

    def get_data_dump(self) -> dict:
        data_dump = super().get_data_dump()

        for field_name in self.pk_fields:
            data_dump[field_name] = getattr(self.obj, '{}_id'.format(field_name)).hex

        return data_dump
