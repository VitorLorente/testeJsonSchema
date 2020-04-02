import json

from contato.models import Contact, ContactFields


class ContactParser(object):
    
    def __init__(self, file_path, layout):

        self.file_path = file_path
        self.contact_fields = ContactFields.objects.get(pk=layout)
        self.layout = self.contact_fields.fields
        self.file_lines = list()
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
        self.get_file_lines()
        self.parser()
        self.bulk_create_contacts()


    def get_file_lines(self):
        
        """
        Apenas separa as linhas do arquivo para parsear uma de cada vez.
        
        """
        with open(self.file_path, 'r') as contact_file:
            self.file_lines = [line for line in contact_file]
            contact_file.close()


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
                'fields_type': contact_fields_pk
                'contact_infos':json.dumps({

                    key: {
                        
                        'verbose_name': self.layout[key]['verbose_name'],
                        'value': line[
                            self.layout[key]['slice_tuple'][0]:self.layout[key]['slice_tuple'][1]
                        ]

                    }
                })

                for key in keys_to_parse
            }

            for line in self.file_lines
        ]


        def bulk_create_contacts(self):
            
            with tempfile.NamedTemporaryFile(
                suffix='.csv',
                prefix=('contact'),
                delete=True,
                mode='w+'
            ) as csv_file:
                filewriter = csv.writer(csv_file, delimiter=',')
                csv_headers = ['fields_type', 'contact_infos']
                csv_writer = csv.DictWriter(csv_file, fieldnames=csv_headers)

                csv_writer.writeheader()
                
                for contact in self.parsed_contacts:
                    csv_writer.writerow(contact)

                Contact.objects.from_csv(
                    csv_file.name
                )
