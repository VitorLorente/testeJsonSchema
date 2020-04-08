from collections import Iterable
from validr import T, Compiler, Invalid

from contato.models import ContactFields, Contact


def validate_fields(instance, layout_type):
    import pdb; pdb.set_trace()

    schema = Compiler().compile(
        generate_fields_schema(
            layout_type
        )
    )
    try:
        schema(instance)
        return True
    except:
        return False
    


def generate_fields_schema(layout_type):
    SUBFIELD_VALIDATE = Contact.SUBFIELD_VALIDATE
    INSTANCE_FIELDS = layout_type.fields

    dict_schema = {
        "$self": "dict",
    }

    # fields_schema = {
    #     key: {
    #         subkey: [f"list.maxlen({len(SUBFIELD_VALIDATE[subkey])})"] + [i for i in set(SUBFIELD_VALIDATE[subkey])] 
    #         if (isinstance(SUBFIELD_VALIDATE[subkey], Iterable) and not 
    #             isinstance(SUBFIELD_VALIDATE[subkey], str))

    #         else SUBFIELD_VALIDATE[subkey]

    #         for subkey in SUBFIELD_VALIDATE.keys()
    #     }

    #     for key in FIELDS.keys()
    # }

    fields_schema = {
        key: {
            subkey: f"{SUBFIELD_VALIDATE[subkey]}.minlen({1 if INSTANCE_FIELDS[key]['requirement'] else 0})"
            if SUBFIELD_VALIDATE[subkey] == "str"

            else SUBFIELD_VALIDATE[subkey]

            for subkey in SUBFIELD_VALIDATE.keys()
        }

        for key in INSTANCE_FIELDS.keys()
    }

    dict_schema.update(fields_schema)
    schema = T(dict_schema)

    return schema