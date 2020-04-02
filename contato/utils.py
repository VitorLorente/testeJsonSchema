def validate_fields(contact):
    """
    Este método verifica se o json submetido para Contact possui todos os campos
    exigidos pelo seu respectivo ContactFields.

    Verifica também se um dos campos está vaio.
    
    TODO: [SÓ FALTA TESTAR] No json de ContactFields deverá constar a informação da obrigatoriedade
    do campo.
    
    """
    validation_keys = set(contact.fields_type.fields.keys())
    contact_keys = set(contact.contact_infos.keys())
    
    if len(validation_keys ^ contact_keys) > 0:
        return False

    for key in validation_keys:
        if (contact.fields_type.fields[key]['requirement'] and not
            contact.contact_infos.get(key, None) and not
            contact.contact_infos.get(key, None) != ''):
            return False

    return True