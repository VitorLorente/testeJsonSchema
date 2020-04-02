from django.contrib.postgres.fields import JSONField
from django.db import models

from postgres_copy import CopyManager

from testeJsonSchema import utils as global_utils


class ContactFields(models.Model):
    SUBFIELD_VALIDATE = {
        'requirement': bool,
        'verbose_name': str,
        'slice_tuple': (int, int)
    }

    name = models.CharField(
        verbose_name="Nome do modelo",
        max_length=10,
    )

    fields = JSONField()


    objects = CopyManager()


    def __str__(self):
        return self.name

    def self_validate(self):

        for key in self.fields.items():
            requirement = key[1].get('requirement', None)
            verbose_name = key[1].get('verbose_name', None)
            slice_tuple = key[1].get('slice_tuple', None)

            # Se houver a tupla exigida, colhe o tipo de parametro dos elementos 
            if slice_tuple:
                slice_params = slice_tuple[0]
            else:
                return False

            # Confere se cada informação está preenchida
            if not (requirement is not None and verbose_name is not None and slice_params is not None):
                return False

            # Confere se as chaves estão ok
            if len(set(key[1].keys()) ^ set(self.SUBFIELD_VALIDATE.keys())) > 0:
                return False

            # Confere se o valor de cada chave tem o tipo certo
            if not (type(requirement) == self.SUBFIELD_VALIDATE['requirement'] and
                type(verbose_name) == self.SUBFIELD_VALIDATE['verbose_name'] and
                type(slice_params) == type(self.SUBFIELD_VALIDATE['slice_params'])):
                    return False

        return True

    def get_fields(self):
        return global_utils.dotdict(self.fields)


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

