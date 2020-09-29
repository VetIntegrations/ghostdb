import string
from datetime import datetime
from hashlib import sha512
from random import choice

from ghostdb.core.event import event
from ghostdb.db.models import user
from .utils import base
from .user_actions import create as create_act, update as update_act


class UserAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.UserCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.UserUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )

    @classmethod
    def set_password(cls, _user: user.User, new_password: str, secret_key: str):
        _user.salt = ''.join([choice(string.printable[:-5]) for i in range(32)])
        _user.password = cls.get_password_hashsum(new_password, _user.salt, secret_key)
        _user.last_changed_password = datetime.utcnow()

    @staticmethod
    def get_password_hashsum(password: str, salt: str, secret_key: str) -> str:
        hashsum = sha512(
            ('$'.join([salt, password, secret_key])).encode('utf-8')
        )

        return hashsum.hexdigest()
