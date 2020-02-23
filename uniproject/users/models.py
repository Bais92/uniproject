from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models


class User(AbstractUser):

    name = CharField(_("Name of User"), blank=True, max_length=255)

    def __str__(self):
        return '%s %s' % self.user.last_name, self.user.first_name

