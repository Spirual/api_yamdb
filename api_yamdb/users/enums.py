from enum import Enum


class UserRole(Enum):
    ADMIN = 'admin', 'admin'
    MODERATOR = 'moderator', 'moderator'
    USER = 'user', 'user'

    @classmethod
    def choices(cls):
        # Django ожидает кортеж (value, human_readable_name).
        return [(role.value[0], role.value[1]) for role in cls]
