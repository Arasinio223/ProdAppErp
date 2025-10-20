from main.models import Uzytkownik
from django.contrib.auth.hashers import make_password

try:
    user = Uzytkownik.objects.get(username='admin')
    user.password = make_password('admin')
    user.save()
    print("Password for admin set successfully")
except Uzytkownik.DoesNotExist:
    print("User 'admin' does not exist")
