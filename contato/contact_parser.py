from contato.models import Contact, ContactFields


class ContactParser(object):
    
    def __init__(self, file_path, layout):
        self.file_path = file_path
        self.layout = ContactFields.objects.get(pk=layout).fields
        self.file_lines = list()
        self.parsed_contacts = dict()

    
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
            ...
        ]

        """
        keys_to_parse = self.layout.keys()

        self.parsed_contacts = [
            
            {
                key: {
                    
                    'verbose_name': self.layout[key]['verbose_name'],
                    'value': line[
                        self.layout[key]['slice'][0]:self.layout[key]['slice'][1]
                    ]

                }

                for key in keys_to_parse
            }

            for line in self.file_lines
        ]


        def bulk_create_contacts(self):
            """
            Método responsável por salvar em lote os contatos. Por performance,
            utilizamos o método COPY do postgres, através do comando .from_csv(),
            da lib django-postgres-copy.
            
            """
            pass