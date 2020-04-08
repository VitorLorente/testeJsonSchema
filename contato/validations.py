from collections import Iterable
from validr import T
from contato.models import ContactFields

def generate_fields_schema(layout_type):
    SUBFIELD_VALIDATE = layout_type.SUBFIELD_VALIDATE
    FIELDS = layout_type.fields

    dict_schema = {
        "$self": "dict",
    }

    fields_schema = {
        key: {
            subkey: [f"list.maxlen({len(SUBFIELD_VALIDATE[subkey])})"] + [i for i in set(SUBFIELD_VALIDATE[subkey])] 
            if (isinstance(SUBFIELD_VALIDATE[subkey], Iterable) and not 
                isinstance(SUBFIELD_VALIDATE[subkey], str))

            else SUBFIELD_VALIDATE[subkey]

            for subkey in SUBFIELD_VALIDATE.keys()
        }

        for key in FIELDS.keys()
    }
    dict_schema.update(fields_schema)
    schema = T(dict_schema)
    return schema