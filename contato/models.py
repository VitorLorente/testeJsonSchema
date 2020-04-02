from django.contrib.postgres.fields import JSONField
from django.db import models

from testeJsonSchema import utils as global_utils


class ContactFields(models.Model):
    SUBFIELD_VALIDATE = {
        'requirement': bool,
        'verbose_name': str,
        'value': str
    }

    name = models.CharField(
        verbose_name="Nome do modelo",
        max_length=10,
    )

    fields = JSONField()


    def __str__(self):
        return self.name

    def self_validate(self):
        status = True

        for key in self.fields.items():

            requirement = key[1]['requirement']
            verbose_name = key[1]['verbose_name']
            value = key[1]['value']

            # Confere se as chaves estão ok
            if set(key[1].keys()) ^ set(SUBFIELD_VALIDATE.keys()) > 0:
                status = False

            # Confere se o valor de cada chave tem o tipo certo
            if not (type(requirement) == SUBFIELD_VALIDATE['requirement'] and
                type(verbose_name) == SUBFIELD_VALIDATE['verbose_name'] and
                type(value) == SUBFIELD_VALIDATE['value']):
                status = False

            # Confere se cada informação está preenchida
            if not (requirement and verbose_name and value):
                status = False

            return status


            



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

