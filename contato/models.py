from django.contrib.postgres.fields import JSONField
from django.db import models

from testeJsonSchema import utils as global_utils


class ContactFields(models.Model):

    name = models.CharField(
        verbose_name="Nome do modelo",
        max_length=10,
    )

    fields = JSONField()


    def __str__(self):
        return self.name


class Contact(models.Model):
    
    fields_type = models.ForeignKey(
        ContactFields,
        on_delete=models.CASCADE,
    )

    upload_date = models.DateField(
        verbose_name='Data de upload',
        auto_now=True
    )

    contact_infos = JSONField()


    def __str__(self):
        return self.infos.first_name + " " + self.infos.last_name

    @property
    def infos(self):
        return global_utils.dotdict(self.contact_infos)

