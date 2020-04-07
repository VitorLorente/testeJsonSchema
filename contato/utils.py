import json
from contato.models import Contact

def validate_fields(contact, contact_layout):
    """
    Este método verifica se o json submetido para Contact possui todos os campos
    exigidos pelo seu respectivo ContactFields.

    Verifica também se há algum campo vazio.
    
    TODO: Implementar validação dos campos mais aninhados.
    
    """
    contact = json.loads(contact['contact_infos'])

    validation_keys = set(contact_layout.fields.keys())
    contact_keys = set(contact.keys())
    
    if len(validation_keys ^ contact_keys) > 0:
        return False

    for key in validation_keys:
        if contact_layout.fields[key]['requirement']:
            if not contact.get(key, None):
                return False
            if not contact.get(key).get('value', None):
                return False

    return True and validate_subfields(contact, contact_layout)


def validate_subfields(contact, contact_layout):
    """
    
    """
    subfields_validate = Contact.SUBFIELD_VALIDATE
    validation_keys = subfields_validate.keys()
    subfields = [contact[key] for key in contact_layout.fields.keys()]

    for key in subfields:
        value = key.get('value', None)
        verbose_name = key.get('verbose_name', None)        

        # Confere se cada informação está preenchida
        if not (value is not None and verbose_name is not None):
            return False

        # Confere se as chaves estão ok
        if len(set(key.keys()) ^ set(validation_keys)) > 0:
            return False

        # Confere se o valor de cada chave tem o tipo certo
        if not (type(value) == subfields_validate['value'] and type(verbose_name) == subfields_validate['verbose_name']):
            return False

    return True
