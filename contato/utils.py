def validate_fields(contact):
    """
    Este método verifica se o json submetido para Contact possui todos os campos
    exigidos pelo seu respectivo ContactFields.

    Verifica também se há algum campo vazio.
    
    TODO: Implementar validação dos campos mais aninhados.
    
    """

    validation_keys = set(contact.fields_type.fields.keys())
    contact_keys = set(contact.contact_infos.keys())
    
    if len(validation_keys ^ contact_keys) > 0:
        return False

    for key in validation_keys:
        if (contact.fields_type.fields[key]['requirement'] and not
            contact.contact_infos.get(key, None)):
            return False

    return True and validate_subfields(contact)


def validate_subfields(contact):
    """
    
    """

    validation_keys = contact.SUBFIELD_VALIDATE.keys()
    subfields = [contact.contact_infos[key] for key in contact.fields_type.fields.keys()]

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
        if not (type(value) == contact.SUBFIELD_VALIDATE['value'] and
            type(verbose_name) == contact.SUBFIELD_VALIDATE['verbose_name']):
                return False

    return True
