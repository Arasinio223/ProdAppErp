
from django.db import models
from django.contrib.auth.models import AbstractUser

class Uzytkownik(AbstractUser):
    pin = models.CharField(max_length=128, null=True, blank=True)
    rfid_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    stawka_godzinowa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class ZlecenieProdukcyjne(models.Model):
    nazwa = models.CharField(max_length=255)
    numer = models.CharField(max_length=255, unique=True)
    klient = models.CharField(max_length=255)
    aktywne = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa

class StatusPracy(models.Model):
    nazwa = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nazwa

class DziennikZdarzenRCP(models.Model):
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(StatusPracy, on_delete=models.CASCADE)
    zlecenie = models.ForeignKey(ZlecenieProdukcyjne, on_delete=models.CASCADE, null=True, blank=True)
