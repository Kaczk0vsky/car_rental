from django.db import models
from django.utils.timezone import now

class Ubezpieczenie(models.Model):
    nazwa = models.CharField(max_length=255)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    kraj = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa


class Marka(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa


class Wypozyczalnia(models.Model):
    miasto = models.CharField(max_length=255)
    kod_pocztowy = models.CharField(max_length=20)
    ulica = models.CharField(max_length=255)
    nr_telefonu = models.CharField(max_length=15)
    numer_budynku = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.miasto}, {self.ulica} {self.numer_budynku}"


class Samochod(models.Model):
    ubezpieczenie = models.ForeignKey(Ubezpieczenie, on_delete=models.SET_NULL, null=True, blank=True)
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE)
    wypozyczalnia = models.ForeignKey(Wypozyczalnia, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    rok_produkcji = models.IntegerField()
    stan_techniczny = models.CharField(max_length=255)
    cena_za_dzien = models.FloatField()

    def __str__(self):
        return f"{self.marka.nazwa} {self.model} ({self.rok_produkcji})"


class Klient(models.Model):
    pesel = models.CharField(max_length=11, unique=True)
    imie = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    email = models.EmailField()
    nr_telefonu = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Platnosc(models.Model):
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    metoda = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.kwota} PLN - {self.metoda}"


class Wypozyczenie(models.Model):
    wypozyczalnia = models.ForeignKey(Wypozyczalnia, on_delete=models.CASCADE)
    samochod = models.ForeignKey(Samochod, on_delete=models.CASCADE)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    platnosc = models.ForeignKey(Platnosc, on_delete=models.SET_NULL, null=True, blank=True)
    data_w = models.DateField()
    data_z = models.DateField()
    koszt = models.DecimalField(max_digits=10, decimal_places=2)
    zaplacono = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"Wypożyczenie {self.samochod} dla {self.klient}"

class Oddzial(models.Model):
    miasto = models.CharField(max_length=255)
    kod_pocztowy = models.CharField(max_length=20)
    ulica = models.CharField(max_length=255)
    nr_telefonu = models.CharField(max_length=15)
    numer_budynku = models.CharField(max_length=10)

    def __str__(self):
        return f"Oddział: {self.miasto}, {self.ulica}"


class Pracownik(models.Model):
    pesel = models.CharField(max_length=11, unique=True)
    oddzial = models.ForeignKey(Oddzial, on_delete=models.CASCADE)
    wypozyczalnia = models.ForeignKey(Wypozyczalnia, on_delete=models.CASCADE)
    imie = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    nr_telefonu = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Pensja(models.Model):
    pracownik = models.ForeignKey(Pracownik, on_delete=models.CASCADE)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    metoda_platnosci = models.CharField(max_length=50)

    def __str__(self):
        return f"Pensja dla {self.pracownik.imie} {self.pracownik.nazwisko}: {self.kwota} PLN"