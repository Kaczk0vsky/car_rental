# Uzywany na poczatku program sluzacy do dodania podstawowych elementow do bazy danych
# Uruchomić należy go tylko raz!

import sqlite3
  
# Polaczenie do bazy danych
conn = sqlite3.connect('db.sqlite3')

# Utworzenie kursora do dodawania do bazy danych
cursor = conn.cursor()

# Dodawanie elementow do bazy danych
# Ubezpieczenie
cursor.execute("INSERT INTO wypozyczenia_ubezpieczenie (nazwa, cena, kraj) VALUES ('Ubezpieczenie Podróżne', 250.75, 'Polska')")
cursor.execute("INSERT INTO wypozyczenia_ubezpieczenie (nazwa, cena, kraj) VALUES ('Ubezpieczenie Zdrowotne', 499.99, 'Niemcy')")
cursor.execute("INSERT INTO wypozyczenia_ubezpieczenie (nazwa, cena, kraj) VALUES ('Ubezpieczenie Samochodowe', 799.50, 'Francja')")
# Marka
cursor.execute("INSERT INTO wypozyczenia_marka (nazwa) VALUES ('Porsche')")
cursor.execute("INSERT INTO wypozyczenia_marka (nazwa) VALUES ('Volkswagen')")
cursor.execute("INSERT INTO wypozyczenia_marka (nazwa) VALUES ('BMW')")
# Wypozyczalnia
cursor.execute("INSERT INTO wypozyczenia_wypozyczalnia (miasto, kod_pocztowy, ulica, nr_telefonu, numer_budynku) VALUES ('Warszawa', '00-001', 'Marszałkowska', '123456789', '10A')")
cursor.execute("INSERT INTO wypozyczenia_wypozyczalnia (miasto, kod_pocztowy, ulica, nr_telefonu, numer_budynku) VALUES ('Kraków', '30-002', 'Floriańska', '987654321', '5B')")
# Samochód
cursor.execute("INSERT INTO wypozyczenia_samochod (ubezpieczenie_id, marka_id, wypozyczalnia_id, model, rok_produkcji, stan_techniczny, cena_za_dzien) VALUES (1, 1, 1, '911 Turbo', 2022, 'Bardzo dobry', 299.90)")
cursor.execute("INSERT INTO wypozyczenia_samochod (ubezpieczenie_id, marka_id, wypozyczalnia_id, model, rok_produkcji, stan_techniczny, cena_za_dzien) VALUES (2, 2, 1, 'Golf GTI', 2020, 'Dobry', 139.90)")
cursor.execute("INSERT INTO wypozyczenia_samochod (ubezpieczenie_id, marka_id, wypozyczalnia_id, model, rok_produkcji, stan_techniczny, cena_za_dzien) VALUES (3, 3, 2, 'M5 Competition', 2021, 'Bardzo dobry', 184.90)")
cursor.execute("INSERT INTO wypozyczenia_samochod (ubezpieczenie_id, marka_id, wypozyczalnia_id, model, rok_produkcji, stan_techniczny, cena_za_dzien) VALUES (NULL, 1, 2, 'Cayenne', 2019, 'Dobry', 239.90)")
cursor.execute("INSERT INTO wypozyczenia_samochod (ubezpieczenie_id, marka_id, wypozyczalnia_id, model, rok_produkcji, stan_techniczny, cena_za_dzien) VALUES (1, 2, 1, 'Passat B8', 2018, 'Średni', 99.90)")
# Klient
cursor.execute("INSERT INTO wypozyczenia_klient (pesel, imie, nazwisko, email, nr_telefonu) VALUES ('89012345678', 'Adam', 'Nowak', 'adam.nowak@example.com', '600700800')")
cursor.execute("INSERT INTO wypozyczenia_klient (pesel, imie, nazwisko, email, nr_telefonu) VALUES ('95082004023', 'Jan', 'Kowalski', 'jan.ko23@wp.pl', '896432998')")
# Platnosc
cursor.execute("INSERT INTO wypozyczenia_platnosc (kwota, data, metoda) VALUES (200.50, '2025-01-29', 'Przelew')")
# Wypozyczenia
cursor.execute("INSERT INTO wypozyczenia_wypozyczenie (wypozyczalnia_id, samochod_id, klient_id, platnosc_id, data_w, data_z, koszt) VALUES (1, 1, 1, 1, '2025-01-29', '2025-02-05', 1000.00)")
# Oddzial
cursor.execute("INSERT INTO wypozyczenia_oddzial (miasto, kod_pocztowy, ulica, nr_telefonu, numer_budynku) VALUES ('Warszawa', '00-001', 'Marszałkowska', '123456789', '10A')")
# Pracownik
cursor.execute("INSERT INTO wypozyczenia_pracownik (pesel, oddzial_id, wypozyczalnia_id, imie, nazwisko, nr_telefonu) VALUES ('12345678901', 1, 1, 'Jan', 'Kowalski', '987654321')")
cursor.execute("INSERT INTO wypozyczenia_pracownik (pesel, oddzial_id, wypozyczalnia_id, imie, nazwisko, nr_telefonu) VALUES ('98203007178', 1, 2, 'Adam', 'Nosalski', '279300412')")
# Pensja
cursor.execute("INSERT INTO wypozyczenia_pensja (pracownik_id, kwota, metoda_platnosci) VALUES (1, 5000.00, 'Przelew')")
cursor.execute("INSERT INTO wypozyczenia_pensja (pracownik_id, kwota, metoda_platnosci) VALUES (2, 6200.00, 'Przelew')")

# Zatwierdzenie i zapisanie zmian w bazie danych    
conn.commit() 
  
# Zakonczenie polaczenia z baza danych
conn.close()