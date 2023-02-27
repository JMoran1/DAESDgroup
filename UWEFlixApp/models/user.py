from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    class Role(Enum):
        CINEMA_MANAGER = 'M'
        ACCOUNT_MANAGER = 'A'
        CLUB_REP = 'R'
        CUSTOMER = 'C'

    role = models.CharField(
        max_length=1,
        choices=[(tag, tag.value) for tag in Role]  # unpack Enum choices
    )
