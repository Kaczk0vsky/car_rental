from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Samochod, Wypozyczenie, Klient, Platnosc, Wypozyczalnia
from django.utils import timezone
from decimal import Decimal

def klient_login(request):
    # Widok logowania klienta
    if request.method == "POST":    # metoda ktora uaktywnia sie po kliknięciu przycisku na stronie, w tym wypadku zaloguj
        # pobranie danych z pol na stronie
        email = request.POST["email"]
        pesel = request.POST["pesel"]
        try:
            # sprawdzenie czy istnieje taki klient jak te dane ktore zostaly podane
            klient = Klient.objects.get(email=email, pesel=pesel)
            request.session['klient_id'] = klient.id
            # jeśli klient podal wszystko prawidlowo przekierowanie do listy z samochodami
            return redirect('lista_samochodow')
        except Klient.DoesNotExist:
            # Jeśli klient nie ma swojego konta lub pomylono dane do logowania - powrot do logowania
            return render(request, "klient_login.html", {"error": "Niepoprawne dane logowania"})
    return render(request, "klient_login.html")

def lista_samochodow(request):
    # Widok z listą samochodów
    samochody = Samochod.objects.all()  # pobranie listy samochodow - all pobiera wszystkie samochody - raw sql: SELECT * FROM wypozyczenia_samochod;
    wypozyczalnie = Wypozyczalnia.objects.all() #pobranie listy wypozyczalni - all pobiera wszystkie samochody - raw sql: SELECT * FROM wypozyczenia_wypozyczalnia;
    # Przekazanie pobranych danych do widoku lista_samochodow.html
    return render(request, "lista_samochodow.html", {'samochody': samochody, 'wypozyczalnie': wypozyczalnie})

def wypozycz(request):
    # jezeli uzytkownik jest zalogowany to wszystko w normie
    if 'klient_id' not in request.session:
        return redirect('klient_login')  # Jeśli użytkownik nie jest zalogowany, przekieruj go do logowania

    klient = get_object_or_404(Klient, id=request.session['klient_id'])  # pobranie zalogowanego klienta
    # samochody = Samochod.objects.all() # pobranie listy samochodow - all pobiera wszystkie samochody - raw sql: SELECT * FROM wypozyczenia_samochod;

    if request.method == "POST": # metoda ktora uaktywnia sie po kliknięciu przycisku na stronie, w tym wypadku Wypozycz
        #pobranie danych z odpowiednich pol czyli:
        samochody_wybrane = request.POST.getlist('samochody') #checkboxów
        data_w = request.POST['data_wypozyczenia']  # pola z  data w
        data_z = request.POST['data_zwrotu']    # pola z data z

        # Logika wypożyczenia - każdy wybrany samochód tworzy obiekt Wypozyczenie w bazie danych
        for samochod_id in samochody_wybrane:   # za kazdy zaznaczony samochod we wszystkich samochodach
            samochod = get_object_or_404(Samochod, id=samochod_id)  # sprawdzamy czy istnieje taki samochod w bazie danych
            wypozyczalnia = samochod.wypozyczalnia  #pobieramy nazwe wypozyczalnie z ktorej pochodzi aktualnie wybrany samochod
            koszt = samochod.cena_za_dzien * (int(data_z.split('-')[2]) - int(data_w.split('-')[2]))    #obliczamy koszt wypozyczenia
            # tworzymy obiekt wyporzyczenie w bazie danych na pdostawie pobranych informacji
            Wypozyczenie.objects.create(
                samochod=samochod,
                klient=klient,
                data_w=data_w,
                data_z=data_z,
                koszt=koszt,
                wypozyczalnia=wypozyczalnia
            )
        # przkierwanie do widoku z podsumowaniem po poprawnie zakonczonej procedurze
        return redirect('wypozyczenie_podsumowanie')
    # # wyswietlenie widoku z wszystkimi wypozyczonymi samochodami dla danego klienta
    # return render(request, 'wypozyczalnia/wypozycz.html', {'samochody': samochody})

def wypozyczenie_podsumowanie(request):
    if 'klient_id' not in request.session:
        return redirect('klient_login')  # sprawdzenie czy użytkownik jest zalogowany

    klient = get_object_or_404(Klient, id=request.session['klient_id'])  # Pobranie zalogowanego klienta
    wypozyczenia = Wypozyczenie.objects.filter(klient=klient) # pobranie wszystkich wypozyczen dla danego klienta
    
    # pobranie danych z wypozyczeniami dla danego klienta i umieszczenie ich w widoku
    return render(request, 'wypozyczenie_podsumowanie.html', {'wypozyczenia': wypozyczenia})

def sprawdz_dostepnosc(request, samochod_id):
    # Funkcja do sprawdzania czy samochód jest dostępny
    data_od = request.GET.get('data_od')    # pobranie daty od
    data_do = request.GET.get('data_do')    # pobranie daty do
    
    with connection.cursor() as cursor:
        # Sprawdzenie dostepnosci samochodu funkcja w SQL
        cursor.execute("""
            SELECT COUNT(*) 
            FROM wypozyczenia_wypozyczenie 
            WHERE samochod_id = %s 
            AND (
                (data_w <= %s AND data_z >= %s) OR
                (data_w <= %s AND data_z >= %s)
            );
        """, [samochod_id, data_do, data_od, data_od, data_do]) # tam gdzie są % kolejno są umieszczane dane z tej tablicy
        # jezeli jakis samochod spelnia wynik to jest dostepny
        dostepny = cursor.fetchone()[0]
        wiadomosc = "Samochód nie jest dostępny"
        if dostepny == 0:
            wiadomosc = "Samochód jest dostępny do wypożyczenia"
    # przekierowanie na strone z wynikiem dostepnosci i przeslanie tam danych odnosnie id samochodu dat i wiadomosci
    return redirect('sprawdz_dostepnosc_wynik', samochod_id=samochod_id, wiadomosc=wiadomosc, data_od=data_od, data_do=data_do)

def sprawdz_dostepnych_pracownikow(request, wypozyczalnia_id):
    # Funkcja sprawdza jacy pracownicy są dostępni w jakiej wypożyczalni
    with connection.cursor() as cursor:
        # pobranie listy pracowników w zależnosci od tego jaka wypozyczalnia zostala wybrana w widoku
        cursor.execute("""
            SELECT id, imie, nazwisko, nr_telefonu
            FROM wypozyczenia_pracownik 
            WHERE wypozyczalnia_id = %s
        """, [wypozyczalnia_id])
        pracownicy = cursor.fetchall()

    # jezeli są jacyś pracownicy to przekierwanie do listy z nimi, a jeżeli nie to powrót do listy samochodów
    if pracownicy:
        return render(request, 'dostepni_pracownicy.html', {'pracownicy': pracownicy})
    else:
        return render(request, 'lista_samochodow.html')

def sprawdz_dostepnosc_wynik(request, samochod_id, wiadomosc, data_od, data_do):
    # Widok wyświetlający wynik sprawdzenia dostępności
    samochod = get_object_or_404(Samochod, id=samochod_id)
    # wybiera widok wynik_dostepnosci i wyswietla tam potrzebne dane takie jak model samochodu daty i wiadomosc
    return render(request, 'wynik_dostepnosci.html', {
        'samochod': samochod.model,
        'wiadomosc': wiadomosc,
        'data_od': data_od,
        'data_do': data_do
    })

def zaplac(request):
    # symulacja placenia za wypozyczony samochod
    if 'klient_id' not in request.session:  # jezeli klient nie jest zalogowany to powrot to logowania
        return redirect('klient_login')

    if request.method == "POST":    # jezeli nacisnieto przycisk zaplac to wywolywany jest ten warunek
        # Pobieranie wybranych wypożyczeń z formularza
        wypozyczenia_ids = request.POST.getlist('wypozyczenia') # pobranie id wypozyczalni wybranej z listy
        wypozyczenia = Wypozyczenie.objects.filter(id__in=wypozyczenia_ids) # sprawdzenie czy jest taka wypozyczalnia i pobranie jej z bazy danych
        #SELECT * FROM app_wypozyczenie WHERE id IN (%s, %s, %s, ...); # surowa komenda z sql
        kwota = sum([wypozyczenie.koszt for wypozyczenie in wypozyczenia]) # zsumowanie calkowitej kowty
        metoda_platnosci = request.POST.get('metoda') # pobranie metody platnosci z pola wyboru

        # tworzenie nowego obiektu Platnosc w bazie danych
        Platnosc.objects.create(
            kwota=Decimal(kwota),
            data=timezone.now().date(),
            metoda=metoda_platnosci
        )

        # aktualizacja statusu wypożyczeń
        for wypozyczenie in wypozyczenia:
            wypozyczenie.zaplacono = True
            wypozyczenie.save()
    # odswiezenie strony z podsumowaniem wypozyczen
    return redirect('wypozyczenie_podsumowanie')