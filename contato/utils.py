def validate_fields(contact):
    validation_keys = set(contact.fields_type.fields.keys())
    contact_keys = set(contact.contact_infos.keys())
    status = True
    
    if len(validation_keys ^ contact_keys) > 0:
        status = False

    for key in validation_keys:
        if not contact.contact_infos.get(key, None):
            status = False

    return status