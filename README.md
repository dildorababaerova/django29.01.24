# django29.01.24
<!-- 
django projecti
python -m venv venv
Luodaan joku file esim. a.py
Jos ei toimi
venv/Scripts/Activate.ps1
tai Command Promp:iin kirjoitetaan 

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
pip install django
django-admin startproject sivusto /Huom! sivusto voidaan nimettää itse 
sivusto folder tulee 2, yksi on tyhjä . Tyhjä siirretään ulkopuoleen, nimetään uudelleen
python manage.py runserver
python manage.py startapp kysely Huom! kysely app:n nimi. Oma valinta
python manage.py makemigrations kysely /app:n nimi
python manage.py migrate


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

kysely/urls.py¶

from django.urls import path

from . import views

urlpatterns = [
    path("", views.indeksi, name="index"),
]

kysely apps.py:ssa näkyy urls.py, mutta pitää yhdistää sivuston urls.py:n kanssa

sivusto/urls.py¶

from django.contrib import admin
from django.urls import include, path /Huom! importoidaan include
import kysely.urls /importoitu

urlpatterns = [
    path("kyselyt/", include(kysely.urls)), / Huom! polls vaihdettu kyselyt ja include:n sisällä kysely 
    path("admin/", admin.site.urls),
]

Kun  mennään ositteen http://127.0.0.1:8000/kyselyt  //pitää lisätä '/' jälkeen kyselyt, muista! 

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

Admin sivussa monikot lisätty "s" kijain. Voidaan korjata lisämällä class Meta: model.py tiedostoon. Muista sisennys funktion alle!
class Meta:
    verbose_name="kysymys"
    verbose_name_plural="kysymykset" /Huom! pienillä kirjaimilla

class Meta():
        verbose_name="vaihtoehto"
        verbose_name_plural="vaihtoehdot"

  
Lisätään näkymiä/vews

kysely/views.py¶

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

Uusittu versio

def yksityiskohdat(request, question_id):
    return HttpResponse(f"Katsot juuri kysymystä {question_id}")


def tulokset(request, question_id):
    return HttpResponse(f"Katsot kysymyksen {question_id} tuloksia")


def äänestä(request, question_id):
    return HttpResponse(f"Olet äänestämässä kysymykseen {question_id}")

Huom! Käytettu f(string) muoto 

Liitetään näkymät/views osoitteeseen kysely/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path("", views.indeksi, name="indeksi"),
    path("<int:question_id>/", views.näytä, name="näytä"),
    path("<int:question_id>/tulokset/", views.tulokset, name="tulokset"),
    path("<int:question_id>/aanesta/", views.äänestä, name="äänestä"),
]

Haetaan tietokannasta kysymyksiä

kysely/views.py¶


from django.http import HttpResponse

from .models import Kysymys /voidaan importoida absolutesti from kysely/models.py


def index(request):
    kysymys_lista = Kysymys.objects.order_by("-julkaisupvm")[:2]
    vastaus_teksti = ", ".join([q.teksti for q in kysymys_lista])
    return HttpResponse(vastaus_teksti)

Django:ssa voidaan tehdä pohje/template jotka on html tiedostoa/file mutta sisältää oma django koodia

Luodaan kysely folder:n sisälle uusi folder templates, sen sisälle uusi kansio projektin nimellä kysely. Sen sisälle tulee html file => indeksi.html

kysely/templates/kysely/indeksi.html¶

{% if kysymykset %}
    <ul>
    {% for kysymys in kysymykset %}
        <li><a href="/kysely/{{ question.id }}/">{{ question.teksti }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>Ei kyselyitä.</p>
{% endif %}

Uusitaan indeksi funktio lisämällä kysely/view.py :n 

polls/views.py¶
from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


Huom,uusi versio!

def indeksi(request):
    kysymyslista = Kysymys.objects.order_by("-julkaisupvm")[:2]
    context = {
        "kysymykset": kysymyslista
    }
    return render(request, "kysely/indeksi.html", context)


Selain/brouser ei näy djangon dynamista html. Renderin avulla ajetaan djangon html, 
sen jälkeen näkyy selaimessa. Selain lukee vaan html.


Jos kirjoitetaan http://127.0.0.1:8000/näytä jälkeen sanoja tai numeroita silti sivusto näyttää ,ei ilmoita virheitä.  Senn takia:

kysely/views.py

from django.http import Http404 // Huom importoidaan
from django.shortcuts import render

from .models import Kysymys /Huom! lisätään






def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

//____________________________________
def näytä(request, question_id):
    try:
        kysymys = Kysymys.objects.get(pk=question_id)
    except Kysymys.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "kysely/näytä.html", {"kysymys": kysymys})


templates/kysely => lisätään näytä.html file

{{ question }}
___________________________________
kysely/templates/kysely/näytä.html¶

{{ kysymys }}


Djangossa on get_object_or_404() oma funktio valmiiksi, mitä voi käyttää siihen että, etsii sen objekti teitokannasta. Jos se löytyy, palauttaa sen, jos ei löyty, silloin näyttää virheilmoitusta 404
polls/views.py¶
from django.shortcuts import get_object_or_404, r








-->
