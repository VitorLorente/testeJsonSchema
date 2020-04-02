contact_fields = {
    "rg": {
        "requirement": true,
        "verbose_name": "R.G."
    },
    "cpf": {
        "requirement": false,
        "verbose_name": "CPF"
    },
    "birthday": {
        "requirement": true,
        "verbose_name": "Nascimento"
    },
    "last_name": {
        "requirement": true,
        "verbose_name": "Sobrenome"
    },
    "first_name": {
        "requirement": false,
        "verbose_name": "Nome"
    }
}

contact = {
    "rg": "00.000.000-0",
    "cpf": "000.000.000-00",
    "birthday": "17021993",
    "last_name": "Lorente",
    "first_name": "Vitor"
}

json_contact_fields = {"rg": {"requirement": true, "verbose_name": "R.G.", "slice_tuple": [42, 54]}, "cpf": {"requirement": true, "verbose_name": "CPF", "slice_tuple": [28, 42]}, "birthday": {"requirement": true, "verbose_name": "Nascimento", "slice_tuple": [20, 28]}, "last_name": {"requirement": true, "verbose_name": "Sobrenome", "slice_tuple": [10, 20]}, "first_name": {"requirement": true, "verbose_name": "Nome", "slice_tuple": [0, 10]}}