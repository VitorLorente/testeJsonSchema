from django.contrib.postgres.fields import JSONField
from django.db import models

from contato.models import Contact


class Phone(models.Model):
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE
    )

    phone_infos = JSONField()