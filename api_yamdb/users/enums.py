from enum import Enum


class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
