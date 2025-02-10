from django.contrib import admin
from .models import Samochod, Wypozyczenie, Pracownik, Ubezpieczenie, Marka, Wypozyczalnia, Klient, Platnosc, Oddzial, Pensja

# Register your models here.
admin.site.register(Samochod)
admin.site.register(Wypozyczenie)
admin.site.register(Pracownik)
admin.site.register(Ubezpieczenie)
admin.site.register(Marka)
admin.site.register(Wypozyczalnia)
admin.site.register(Klient)
admin.site.register(Platnosc)
admin.site.register(Oddzial)
admin.site.register(Pensja)