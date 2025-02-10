from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.klient_login, name='klient_login'),
    path("samochody/", views.lista_samochodow, name="lista_samochodow"),
    path('wypozycz/', views.wypozycz, name='wypozycz'),
    path('zaplac', views.zaplac, name='zaplac'),
    path('wypozyczenie/podsumowanie/', views.wypozyczenie_podsumowanie, name='wypozyczenie_podsumowanie'),
    path('sprawdz_dostepnosc/<int:samochod_id>/', views.sprawdz_dostepnosc, name='sprawdz_dostepnosc'),
    path('wynik_dostepnosci/<int:samochod_id>/<str:wiadomosc>/<str:data_od>/<str:data_do>/', views.sprawdz_dostepnosc_wynik, name='sprawdz_dostepnosc_wynik'),
    path('sprawdz_dostepnych_pracownikow/<int:wypozyczalnia_id>/', views.sprawdz_dostepnych_pracownikow, name='sprawdz_dostepnych_pracownikow'),
]
