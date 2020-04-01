from django.contrib.postgres.fields import JSONField
from django.db import models

class Contact(models.Model):
    #
    upload_date = models.DateField(
        verbose_name='Data de upload',
        auto_now=True
    )

    contact_infos = JSONField()