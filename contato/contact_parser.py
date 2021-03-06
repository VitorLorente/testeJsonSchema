import csv
from datetime import date
import json
import tempfile

from contato.models import Contact, ContactFields
# from contato.utils import validate_fields
from contato.validations import generate_fields_schema, validate_fields


class ContactParser(object):
    
    def __init__(self, file_path, contact_fields_pk):

        self.file_path = file_path
        self.contact_fields = ContactFields.objects.get(pk=contact_fields_pk)
        self.layout = self.contact_fields.fields
        self.file_lines = list()
        self.schema = None
        self.parsed_contacts = dict()

    
    def go(self):
        
        """
        Método de gatilho para o parser. É o que será utilizado na task
        do celery.
        Atividades realizadas:
            - separa o arquivo em linhas (lista de strings);
            - parseia o arquivo separando em uma linha de dicionários utilizados
              para gerar o csv usado no .from_csv();
            - Gera um arquivo csv e salva no postgres com .from_csv().
        
        """
        import time
        self.get_file_lines()
        start = time.time()
        self.get_validate_schema()
        end = time.time()
        self.parser()
        self.clean()
        print(end-start)
        self.bulk_create_contacts()

    def get_file_lines(self):
        
        """
        Apenas separa as linhas do arquivo para parsear uma de cada vez.
        
        """
        with open(self.file_path, 'r') as contact_file:
            self.file_lines = [line for line in contact_file]
            contact_file.close()


    def get_validate_schema(self):

        """
        Constrói um schema validador do jsonfield 'contacts_info' (de Contact), baseado no
        jsonfield 'fields' (de ContactFields), populando self.schema para ser usado no
        método clean().

        """
        self.schema = generate_fields_schema(self.contact_fields)


    def parser(self):
        
        """
        Parseia cada linha (cada contato) do arquivo, gerando uma lista
        de dicionários baseados no modelo do contato a ser salvo como
        jsonfield.
        
        self.parsed_contacts = [
            {
                fields_type: contact_fields_pk,
                contact_infos: {
                    'field_1': {
                        verbose_name: 'Field One',
                        value: 'Value from parsed file'
                    },
                    'field_2': {
                        verbose_name: 'Field Two',
                        value: 'Value from parsed file'
                    },
                    ...
                }
            },
            ...
        ]

        """
        keys_to_parse = self.layout.keys()
        contact_fields_pk = self.contact_fields.pk

        self.parsed_contacts = [
            
            {
                'fields_type': contact_fields_pk,
                'upload_date': date.today(),
                'contact_infos': {
                    key: {
                        
                        'verbose_name': self.layout[key]['verbose_name'],
                        'value': line[
                            self.layout[key]['slice_tuple'][0]:self.layout[key]['slice_tuple'][1]
                        ].rstrip()

                    }
                    for key in keys_to_parse
                }

            }

            for line in self.file_lines
        ]


    def clean(self):
        
        """
        

        """

        self.parsed_contacts = [
            instance for instance in self.parsed_contacts
            if validate_fields(instance['contact_infos'], self.schema)
        ]
        for instance in self.parsed_contacts:
            instance['contact_infos'] = json.dumps(instance['contact_infos'])



    def bulk_create_contacts(self):
        
        """
        Cria um csv temporário com .DictWriter a partir dos dicionários em
        self.parsed_contacts. O csv é utilizado do salvamento no banco de dados,
        com .from_csv() da lib django-postgres-copy.

        """
        with tempfile.NamedTemporaryFile(
            suffix='.csv',
            prefix=('contact'),
            delete=True,
            mode='w+'
        ) as csv_file:
            filewriter = csv.writer(csv_file, delimiter=',')
            csv_headers = ['fields_type', 'contact_infos', 'upload_date']
            csv_writer = csv.DictWriter(csv_file, fieldnames=csv_headers)

            csv_writer.writeheader()
            
            for contact in self.parsed_contacts:
                csv_writer.writerow(contact)

            csv_file.read()

            Contact.objects.from_csv(
                csv_file.name
            )
