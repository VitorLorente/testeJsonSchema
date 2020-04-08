from contato.models import Contact
from contato.utils import validate_fields
contact = Contact.objects.all().select_related('fields_type').get()
validate_fields(contact)

from contato.contact_parser import ContactParser
import os
c = ContactParser(os.getcwd()+'/contacts_modelo1.txt', 2)
c.go()

from contato.contact_parser import ContactParser
from contato.models import ContactFields, Contact
import os
path = os.getcwd() + '/contacts_modelo1.txt'
pk_modelo = ContactFields.objects.first().pk
parser = ContactParser(path, pk_modelo)
parser.go()

from contato.models import Contact, ContactFields
from contato.utils import validate_fields
c = Contact.objects.first()
validate_fields(c.contact_infos, c.fields_type)

from contato.models import ContactFields
from contato.validations import generate_subfields_schema
c = ContactFields.objects.first()
generate_subfields_schema(c)
