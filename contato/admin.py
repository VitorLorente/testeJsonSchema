from django.contrib import admin
from contato.models import Contact, ContactFields
from telefone.models import Phone


class PhoneAdmin(admin.ModelAdmin):
    pass
admin.site.register(Phone, PhoneAdmin)


class ContactAdmin(admin.ModelAdmin):
    pass
admin.site.register(Contact, ContactAdmin)


class ContactFieldsAdmin(admin.ModelAdmin):
    pass
admin.site.register(ContactFields, ContactFieldsAdmin)