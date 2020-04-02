from django.contrib.postgres.fields import JSONField
from django.db import models

from testeJsonSchema import utils as global_utils


class ContactFields(models.Model):
    SUBFIELD_VALIDATE = {
        'requirement': bool,
        'verbose_name': str
    }

    name = models.CharField(
        verbose_name="Nome do modelo",
        max_length=10,
    )

    fields = JSONField()


    def __str__(self):
        return self.name

    def self_validate(self):

        for key in self.fields.items():
            requirement = key[1].get('requirement', None)
            verbose_name = key[1].get('verbose_name', None)

            # Confere se cada informação está preenchida
            if not (requirement is not None and verbose_name is not None):
                return False

            # Confere se as chaves estão ok
            if len(set(key[1].keys()) ^ set(self.SUBFIELD_VALIDATE.keys())) > 0:
                return False

            # Confere se o valor de cada chave tem o tipo certo
            if not (type(requirement) == self.SUBFIELD_VALIDATE['requirement'] and
                type(verbose_name) == self.SUBFIELD_VALIDATE['verbose_name']):
                    return False

        return True


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

