
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .models import Uzytkownik, ZlecenieProdukcyjne, StatusPracy, DziennikZdarzenRCP

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        if 'pin' in form.changed_data:
            obj.pin = make_password(obj.pin)
        super().save_model(request, obj, form, change)

admin.site.register(Uzytkownik, CustomUserAdmin)
admin.site.register(ZlecenieProdukcyjne)
admin.site.register(StatusPracy)
admin.site.register(DziennikZdarzenRCP)
