def validate_fields(contact):
    """
    Este método verifica se o json submetido para Contact possui todos os campos
    exigidos pelo seu respectivo ContactFields.

    Verifica também se um dos campos está vaio.
    
    TODO: No json de ContactFields deverá constar a informação da obrigatoriedade
    do campo.
    
    """
    validation_keys = set(contact.fields_type.fields.keys())
    contact_keys = set(contact.contact_infos.keys())
    status = True
    
    if len(validation_keys ^ contact_keys) > 0:
        status = False

    for key in validation_keys:
        if not contact.contact_infos.get(key, None):
            status = False

    return status