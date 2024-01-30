# django29.01.24
<!-- 
django projecti
https://docs.djangoproject.com/en/5.0/intro/tutorial01/ sivustosta aloitetaan projekti
django-admin startproject mysite //tässä mysite projectin nimi 
Aloitetaan tehdä ensimmäinen näkymä 

kysely/views.py¶

from django.http import HttpResponse

def indeksi(request): /Huom! tässä index vaihdettu indeksi
    return HttpResponse("Hello, world. You're at the polls index.") 



Jos haluat kysymyksiä ja vastauksia voidaan käyttää F12 nappi tai Ctrl+Shift+i
 WebDeveloperTools
Network

Näkymä pitää liittää johonkin osoiteeseen 
Luodaan kysely folderin alle file urls.py

kysely/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path("", views.indeksi, name="index"),
]

kysely apps.py:ssa näkyy urls.py, mutta pitää yhdistää sivuston urls.py:n kanssa

sivusto/urls.py

from django.contrib import admin
from django.urls import include, path /Huom! importoidaan include
import kysely.urls /importoitu

urlpatterns = [
    path("kyselyt/", include(kysely.urls)), / Huom! polls vaihdettu kyselyt ja include:n sisällä kysely 
    path("admin/", admin.site.urls),
]

Kun  mennään ositteen http://127.0.0.1:8000/kyselyt pitää lisätä, muista! 

sivusto/settings.py lisätään INSTALLED_APPS => kysely tiedosto

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kysely'
]

Konsolille kirjoitetaan 
python manage.py createsuperuser
Username:admin /itse valitat
Email address: /ei mitään tyhjä
Password:admin
Password(again):
Bypass....[y/N]?: y ja enter

Mennään admin sivulle
Groups /voidaan vaihtaa salasana sekä käyttäjä
Users

Mennään djangon https://docs.djangoproject.com/en/5.0/intro/tutorial02/ sivulle

kysely/models.py¶


from django.db import models


class Kysymys(models.Model):
    teksti = models.CharField(max_length=200)
    julkaisupvm = models.DateTimeField("julkaistu")


class Vaihtoehto(models.Model):
    kysymys = models.ForeignKey(Kysymys, on_delete=models.CASCADE)
    teksti = models.CharField(max_length=200)
    aanet = models.IntegerField(default=0)

Nämät modulit kuvaille mitää tietokantaan pitää tallentaa,käyttänössä tietokantataulu
Jos halutaan katsoa db.sqlite3: ssa VS Extenions paalikoista valitaan SQLite Viewer  

models.py :ssa
class modelit pitää yhdistää ja ForegnKey yhdistetään

kysely/admin.py 

from django.contrib import admin

from .models import Kysymys, Vaihtoehto

admin.site.register(Kysymys)


On mahdollista Vaihtoehtomodelin lisätä kenttä list: kysymys ja teksti
@admin.register(Vaihtoehto)
class VaihtoehtoAdmin(admin.ModelAdmin):
    list_display = ["kysymys", "teksti"]

Vaihdettu TIME_ZONE sekä LANGUAGE_CODE

LANGUAGE_CODE = 'fi'

TIME_ZONE = 'Europe/Helsinki'

Teksti näyttää object:lta, vaihdetaan tekstiksi lisäämällä models.py class:in alle

from django.db import models

class Kysymys(models.Model):
    # ...
    def __str__(self):
        return self.teksti


class Vaihtoehto(models.Model):
    # ...
    def __str__(self):
        return self.teksti

Lisätään näkymiä/vews







-->
