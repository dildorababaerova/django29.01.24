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
manage.py file myös siirretään ulkopuolelle
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

Kun  mennään osdjanitteen http://127.0.0.1:8000/kyselyt  //pitää lisätä '/' jälkeen kyselyt, muista! 

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

Nämät modulit kuvailee mitää tietokantaan pitää tallentaa,käyttänössä tietokantataulu
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

(riittä kun laitetään etusivulle???)

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
from django.shortcuts import get_object_or_404, render

from .models import Question


# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


____________________________________________________________________
kysely/views.py¶


from django.shortcuts import get_object_or_404, render

from .models import Kysymys



def näytä(request, kysymys_id):
    kysym = get_object_or_404(Kysymys, pk=kysymys_id)
    return render(request, "kysely/näytä.html", {"kysymys": kysym})

Kun vaihdettu question_id => kysymys_id:ksi, pitää vaihtaa kysely/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path("", views.indeksi, name="indeksi"),
    path("<int:kysymys_id>/", views.näytä, name="näytä"),
    path("<int:question_id>/tulokset/", views.tulokset, name="tulokset"),
    path("<int:question_id>/aanesta/", views.äänestä, name="äänestä"),
]


Luodaan näytä.html lisämällä templates/kysely folderille

Huom! views.py :ssa question_text vaihdettu kysymys, sen takia vaihdetaan kysymyksi

kysely/templates/kysely/näytä.html¶


<h1>{{ kysymys.teksti}}</h1>    // Huom! Tässä teksti otettu models.py Kysymys class atribuutista, joka on sidottu Vaihtoehto class modelin 
                                //kanssa  ForeignKey:lla
<ul>
{% for valinta in kysymys.vaihtoehto_set.all %}
    <li>{{ valinta.teksti }}</li>
{% endfor %}
</ul>


indeksi.py :ssa huono tapa kirjoittaa ;

<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>

sen paikalle korjataan:

<li><a href="{% url 'näytä' kysym.id %}">{{ kysym.teksti }}</a></li>


Tässä app:ssa on esim. näytä niminen näkymä. Voisi olla toisessakin app:ssa näytä nimenen näkymä. Estetään sekoitusta toisten app:n kanssa lisäämällä app_name = "kysely"


kysely/urls.py¶
from django.urls import path

from . import views

app_name = "kysely"
urlpatterns = [
    path("", views.indeksi, name="indeksi"),
    path("<int:kysymys_id>/", views.näytä, name="näytä"),
    path("<int:question_id>/tulokset/", views.tulokset, name="tulokset"),
    path("<int:question_id>/äänestä/", views.äänestä, name="äänestä"),
]


sekä vaihdetaan;

kysely/templates/kysely/index.html¶

<li><a href="{% url 'näytä' kysym.id %}">{{ kysym.teksti }}</a></li>

kysely/templates/kysely/index.html¶

<li><a href="{% url 'kysely:näytä' kysym.id %}">{{ kysym.teksti }}</a></li>


Luodaan lokeen. Jos lähetetään kysymyksiä palvelimelle, silloin käytetään GET request-
Jos lähetetään lomakkeen kysely, silloin käytetään post request.

GET metodi sisältää vaan url osoitteen. 
Jos POST metodi silloin on mahdollistaa lähettää tiedot, esim. lomakkkeen kentät(Lähettäjän kenttä, palautteen kenttän arvot).

Luodaan lomakkeen:

kysely/templates/kysely/näytä.html¶


<form action="{% url 'kysely:äänestä' kysymys.id %}" method="post">

{% csrf_token %}  // Huom! käyttäjäturvallisuus
<fieldset>

    <legend><h1>{{ kysymys.teksti }}</h1></legend>

    {% if virheviesti %}<p><strong>{{ virheviesti }}</strong></p>{% endif %} // kun virheviesti strong näyttää lihavuutena. error vaihtettu 
                                                                            //virheviestenä tässä sekä views:ssa

    {% for valinta in kysymys.vaihtoehto_set.all %}
        <input type="radio" 
        name="choice" 
        id="vaihtoeht{{ forloop.counter }}" 
        value="{{ valinta.id }}">
        <label for="vaihtoeht{{ forloop.counter }}">{{ valinta.teksti }}</label><br>
    {% endfor %}
</fieldset>
<input type="submit" value="Äänestä">
</form>

Seuraviksessa käsitelty ottaa äänestyksen vaihtoehto vastaan

polls/views.py¶
from django.http import HttpResponse, HttpResponseRedirect //HUom! importoitu
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Vaihtoehto, Kysymys


# ...
def äänestä(request, kysymys_id):  // Huom! vaihdetaan urls:py:ssa myös
    kysym = get_object_or_404(Kysymys, pk=kysymys_id) // Huom! vaihdetaan urls:py:ssa myös
    try:
        valittu = kysym.vaihtoehto_set.get(pk=request.POST["choice"])
    except (KeyError, Vaihtoehto.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "kysely/näytä.html",
            {
                "kysymys": kysym,
                "virheviesti": "Et valinnut mitään",
            },
        )
    else:
        valittu.ääniä += 1
        valittu.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("kysely:tulokset", args=(kysym.id,))) // UUdelleen ohjausta



Seuravaksi tehdään tulokset.html sivu

kysely/views.py¶


from django.shortcuts import get_object_or_404, render


def tulokset(request, kysymys_id):   // Huom! vaihdetaan urls:py:ssa myös
    kysym = get_object_or_404(Kysymys, pk=kysymys_id)   // Huom! vaihdetaan urls:py:ssa myös
    return render(request, "kysely/tulokset.html", {"kysymys": kysym})


Luodaan tulokset.html file

kysely/templates/kysely/tulokset.html¶


<h1>{{ kysymys.teksti }}</h1>

<ul>
{% for vaihtoehto in kysymys.vaihtoehto_set.all %}
    <li>{{ vaihtoehto.teksti }} -- {{ vaihtoehto.ääniä }} ääntä</li>
{% endfor %}
</ul>

<a href="{% url 'kysely:näytä' kysymys.id %}">Äänestätkö uudelleen?</a>


voidaan tehdä generic/yleisiä näkymä. Voidaan selviämään vähemmällä koodeilla samasta asiasta.

kysely/views.py¶


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic // Huom! importoitu

from .models import Vaihtoehto, Kysymys


class ListaNäkymä(generic.ListView):
    nimi = "kysely/indeksi.html"
    objekti_nimi = "kysymykset"

    def get_queryset(self):
        """Palauttaa viimeiset kysymykset."""
        return Kysymys.objects.order_by("-pub_date")[:2]


class NäytäNäkymä(generic.DetailView):
    model = Kysymys
    nimi = "kysely/näytä.html"


class TuloksetNäkymä(generic.DetailView):
    model = Kysymys
    nimi = "kysely/näytä.html"


def äänestä(request, kysymys_id):  // Huom! vaihdetaan urls:py:ssa myös
    kysym = get_object_or_404(Kysymys, pk=kysymys_id) // Huom! vaihdetaan urls:py:ssa myös
    try:
        valittu = kysym.vaihtoehto_set.get(pk=request.POST["choice"])
    except (KeyError, Vaihtoehto.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "kysely/näytä.html",
            {
                "kysymys": kysym,
                "virheviesti": "Et valinnut mitään",
            },
        )
    else:
        valittu.ääniä += 1
        valittu.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("kysely:tulokset", args=(kysym.id,))) // Uudelleen ohjausta



    kysely/urls.py¶


from django.urls import path

from . import views

app_name = "kysely"
urlpatterns = [
    path("", views.ListaNäkymä.as_view(), name="indeksi"),
    path("<int:pk>/", views.NäytäNäkymä.as_view(), name="näytä"),
    path("<int:pk>/tulokset/", views.TuloksetNäkymä.as_view(), name="tulokset"),
    path("<int:kysymys_id>/äänestä/", views.äänestä, name="äänestä"),
]
    ...




Consolissa toimiminen

python manage.py shell

from kysely.models import Kysymys

Kysymys.objects.all()
<QuerySet [<Kysymys: Löysitkö työpaikkaa?>, <Kysymys: Tykkäätkö aurinkoa?>]>
Kysymys.objects.first()
<Kysymys: Löysitkö työpaikkaa?>
>>> k.onko_julkaistu_lähiaikoina()
False // koska lähiaikoina merkitsimme 1 päivä ennen

Asennetaan 
pip install ipython

Kokeillaan test.py

Ensiksi luodaan uusu funktio models.py


Testaus


kysely/models.py¶

import datetime // Huom! import
from django.utils import timezone // Huom! import

def onko_julkaistu_lähiaikoina(self):
        nyt = timezone.now()
        return nyt - datetime.timedelta(days=1) <= self.julkaisupvm <= nyt


kysely/tests.py¶


import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Kysely


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

class KysymysModelTests(TestCase):
    def test_onko_julkaistu_lähiaikoina_tulevaisuuden_kysymyksellä(self):
        """
        onko_julkaistu_lähiaikoina() returns False for questions whose pub_date
        is in the future.
        """
        tulevaisuuden_aika = timezone.now() + datetime.timedelta(days=30)
        tulevaisuuden_kysymys = Kysymys(julkaisupvm=tulevaisuuden_aika)
        vastaus= tulevaisuuden_kysymys.onko_julkaistu_lähiaikoina()
        self.assertIs(vastaus, False)

    def test_onko_julkaistu_lähiaikoina_vanhalla_kysymyksellä(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        päivä_ja_yksi_sek = timezone.now() - datetime.timedelta(days=1, seconds=1)
        vanha_kysymys = Kysymys(julkaisupvm=päivä_ja_yksi_sek)
        self.assertIs(vanha_kysymys.onko_julkaistu_lähiaikoina(), False)


    def test_onko_julkaistu_lähiaikoina_nykyisellä_kysymyksellä(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        vähimmän_kuin_vuorokausi = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        tuore_kysymys = Kysymys(julkaisupvm=vähimmän_kuin_vuorokausi)
        self.assertIs(tuore_kysymys.onko_julkaistu_lähiaikoina(), True)



Client ohjelma jolla voidaan ajaa samoja asia mitä webselain lähetää niitä kyselyitä meidän ohjelmalle. Client:n avulla voidaan lähettää kyselyitä meidän ohjelmalle ja voidaan tutkia mitä vastauksia sieltä saatin. Tutorialissa kokeltu shell:ssa.
Djangon testissa käytettävä asiakas ohjelma, se toimii nyt täällä tavalla, että osoitteet syöttää sinne tekstinä ja sivun sisällön tekstinä. On graafista esitystä, mutta emme nähdä sivua, että se näyttää oikeasti selaimessa. Siihen on oma työkalut miten pystyy sen tekemään, mutta me voidaan tämän avulla voidaan tehdä paljon testaamista. Me pysytytään tarkistamaan, että sieltä tulee oikealainen sivuja ja sivussa oikeanäköinen HTML elementit.

Konsolin annetaan komento:
 python manage.py shell

Konsolin kirjoitetaan:
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
>>> from django.test import Client
>>> client = Client()

>>> # get a response from '/'  // Viittää HTTP protokollan GET metodin

>>> response = client.get("/")

>>> response 
>>> response.status_code
Out[8]: 200
>>> response.content
Out[9]: b'\n    <ul>\n    \n        <li><a href="/2/">Tykk\xc3\xa4\xc3\xa4tk\xc3\xb6 aurinkoa?</a></li>\n    \n        <li><a href="/1/">L\xc3\xb6ysitk\xc3\xb6 ty\xc3\xb6paikkaa?</a></li>\n    \n    </ul>\n'
>>> print(response.content.decode())
<ul>

        <li><a href="/2/">Tykkäätkö aurinkoa?</a></li>

        <li><a href="/1/">Löysitkö työpaikkaa?</a></li>

    </ul>
In [10]: response = client.get("/2/")
In [11]: print(response.content.decode())

<form action="/2/%C3%A4%C3%A4nest%C3%A4/" method="post">
    <input type="hidden" name="csrfmiddlewaretoken" value="Z0Dfr4SZBLcQiDTQsc0Szt6PIaSjM6kakj6cqOR6i4qgAgGwIGWvuO6C0nvbxui7">
    <fieldset>
        <legend><h1>Tykkäätkö aurinkoa?</h1></legend>


            <input type="radio"
            name="valittu"
            id="vaihtoeht1" value="2">
            <label for="vaihtoeht1">Kyllä</label><br>

            <input type="radio"
            name="valittu"
            id="vaihtoeht2" value="3">
            <label for="vaihtoeht2">Ei</label><br>

    </fieldset>
    <input type="submit" value="Äänestä">
</form>

Voidaan nähdä tuloksessa(print), että näytä.html:n koodin mukaan tuli esille. 

response = client.get("/") 
print(response.content.decode())

____________________________________________________________________
djangon tutorial sivusto
Not Found: /
>>> # we should expect a 404 from that address; if you instead see an
>>> # "Invalid HTTP_HOST header" error and a 400 response, you probably
>>> # omitted the setup_test_environment() call described earlier.

>>> response.status_code
404
>>> # on the other hand we should expect to find something at '/polls/'
>>> # we'll use 'reverse()' rather than a hardcoded URL

>>> from django.urls import rev
>>> response = client.get(reverse("kysely:indeksi"))
>>> response.status_code
200
>>> response.content
b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#x27;s up?</a></li>\n    \n    </ul>\n\n'
>>> response.context["kysymykset"]
<QuerySet [<Question: What's up?>]>
_____________________________________________________________________________


Näyttää etusivun. Tässä views.py => class ListäNäkymä:ssä Kysymykset rajoittaa palautettuen kysymysten määrän [:2] eli näyttää vaan 2 kysymystä. Hakeee julkaisun päivämäärän perusteella.("-julkaisupvm") "-" merkki
tarkoittaa uusin päivämäärä tulee esille ensimmäisenä.

Kokeillaan, että rajoittaa sen, jotta julkaistaan  vasta tulevasuudessa, ei näytetään siitä.

Laitetaan serverin käyntiin.
python manage.py runserver
Luodaan uudella pvm:llä kysymys ja vaihtoehdot http://127.0.0.1:8000/admin :ssa.
mutta kun mennään etusivulle siellä näkyy, vaikka tulevaisuuden kysymys.

kysely/views.py

from django.utils import timezone

class ListaNäkymä(generic.ListView):
    template_name = "kysely/indeksi.html"
    context_object_name = "kysymykset"

    def get_queryset(self):
        nyt = timezone.now()

        #Haetaan kaikki kysymykset
        kaikki_kysymykset = Kysymys.objects.all()

        # Suodatetaan (filter) kaikista kysymyksistä ne, joiden julkaisupvm on pienempi tai yhtä suuri 
        # kuin tämänhetkinen aika (muuttujassa "nyt")
        # Huom! lte = Less Than or Equal
        ei_tulevaisuudessa = kaikki_kysymykset.filter(julkaisupvm__lte = nyt).order_by

        # Järjestetään julkaisupvm:n päivämäärän mukaan
        # Huom! "-" merkki edessä kääntää järjestyksen niin, että suuret 
        # arvot tulevat ennen pieniä, jolloin uusimmat kysymykset ovat ensemmäisenä
        järjestetyt_kysymykset=ei_tulevaisuudessa("-julkaisupvm")
        
        return järjestetyt_kysymykset[:2]

Nämät koodit tulivät näkymään class ListaNäkymä: n def get_queryset(self):n. Silla voi rajoittaa ListView :ssa mitä sen Listassa näkyy.

Jos otetaan pois get_queryset() ja kirjoitetaan paikalle model = Kysymys tulee kaikki kysymyksiä.

Kun luodaan uuden folderin test/test_models.py // Huom! test_models.py:ssa importoitu models :n eteen pitäisi laittaa 2"..".
Koska models tulee ylifolderista eli kysely:sta. Se ei ole test folderissa.
Django ei näy test_models.py. Luodaan uusi file __init__.py test folderin sisälle.


test/test_models.py

from django.urls import reverse
from django.utils import timezone
import datetime
from django.test import TestCase
from ..models import Kysymys


def luo_kysymys(teksti, days):
    """
    Create a kysymys with the given `teksti` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    aika = timezone.now() + datetime.timedelta(days=days)
    return Kysymys.objects.create(
        teksti=teksti, 
        julkaisupvm=aika)


class KysymysIndeksiNäkymäTests(TestCase):
    def test_ei_kysymyksiä(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        vastaus = self.client.get(reverse("kysely:indeksi"))
        self.assertEqual(vastaus.status_code, 200)

        #print(vastaus.content) // Huom! voidaan katsoa vastauksen sisältöä

        self.assertContains(vastaus, "Ei kyselyitä saatavilla.")
        self.assertQuerySetEqual(vastaus.context["kysymykset"], [])

    def test_mennyt_kysymys(self):
        """
        Question with a pub_date in the past are displayed on the
        index page.
        """
        kysymys = luo_kysymys(teksti="Mennyt kysymys.", days=-30)
        vastaus = self.client.get(reverse("kysely:indeksi"))
        self.assertQuerySetEqual(
            vastaus.context["kysymykset"],
            [kysymys],
        )

    def test_tuleva_kysymys(self):
        """
        Question pub_date in the future aren't displayed on
        the index page.
        """
        luo_kysymys(teksti="Tuleva kysymys.", days=30)
        vastaus = self.client.get(reverse("kysely:indeksi"))
        self.assertContains(vastaus, "Ei kyselyitä saatavilla.")
        self.assertQuerySetEqual(vastaus.context["kysymykset"], [])

    def test_tuleva_kysymys_ja_mennyt_kysymys(self):
        """
        Even if both past and future kysymyss exist, only past kysymyss
        are displayed.
        """
        kysymys = luo_kysymys(teksti="Mennyt kysymys.", days=-30)
        luo_kysymys(teksti="Mennyt kysymys.", days=30)
        vastaus = self.client.get(reverse("kysely:indeksi"))
        self.assertQuerySetEqual(
            vastaus.context["kysymykset"],
            [kysymys],
        )

    def test_2_mennyttä_kysymystä(self):
        """
        The questions index page may display multiple questions.
        """
        kysymys1 = luo_kysymys(teksti="Mennyt kysymys 1.", days=-30)
        kysymys2 = luo_kysymys(teksti="Mennyt kysymys 2.", days=-5)
        vastaus = self.client.get(reverse("kysely:indeksi"))
        self.assertQuerySetEqual(
            vastaus.context["kysymykset"],
            [kysymys2, kysymys1],
        )
        
        
Testataan NäytäNäkymä 


kysely/views.py

class NäytäNäkymä(generic.DetailView):
    model = Kysymys
    template_name = "kysely/näytä.html"
    
    def get_queryset(self):
        return Kysymys.objects.filter(julkaisupvm__lte=timezone.now())


Lisätään tests/test_views.py 


class KysymysNäytäNäkymäTestit(TestCase):
    def test_tuleva_kysymys(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        tuleva_kysymys = luo_kysymys(teksti="Tuleva kysymys.", days=5)
        osoite = reverse("kysely:näytä", args=(tuleva_kysymys.id,))
        vastaus = self.client.get(osoite)
        self.assertEqual(vastaus.status_code, 404)

    def test_mennyt_kysymys(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        mennyt_kysymys = luo_kysymys(teksti="Mennyt kysymys.", days=-5)
        osoite = reverse("kysely:näytä", args=(mennyt_kysymys.id,))
        vastaus = self.client.get(osoite)
        self.assertContains(vastaus, mennyt_kysymys.teksti)




 Meidän ohjelma lähettää HTML vastauksia, mitkä olimme tehneet python koodilla. Sen lisäksi pystymme lähettää kuvia, JS tai CSS.
 Djangossa puhutaan static fileksi. Pythonilla luotu vastauksia sanotaan dynaamisia vastauksia.

 Lähetään rakentaa ohjeen mukaisesti tyylejä.

 Lisätään kysely/static/kysely/style.css

 
 body {
    background: white url("images/background.jpg") no-repeat;
}

li a {
    color: rgb(44, 28, 212);
}
 li a {
    color: green;
}


kysely/templates/kysely/indeksi.html

{% load static %}

<link rel="stylesheet" href="{% static 'kysely/style.css' %}">



kysely/static/kysely/style.css

luodaan uusi tiedisto images ja sinne lisätään kuvia. Meidän tapaukessa lisätty background.jpg.

Miten pitäisi laittaa palvelimelle. Ei tule django application läpi, static tiedostot tulevat suoraan webserveriltä.
Turha käyttä python koodija. Jos paljon kuvia ja tiedostoja, käytänössä CDN Content Delivery Network palvelu. Voidaan siitä kautta menemään sisältöä esimerkiksi joilta toiselta palvelimelta lähimpänä siitä käyttäää. Staatinen tiedostoa voidaan helppo kopioida.


Jos halutaan eri järjestyksen admin sivulla, päivämäärä näytetään ennen tekstiä:

from django.contrib import admin

from .models import Kysymys


class KysymysAdmin(admin.ModelAdmin):
    kentä = ["julkaisupvm", "teksti"]


admin.site.register(Kysymys, KysymysAdmin)


Kun painetaan vasemmän puolen debug merkki, tulee create a launch.json file. Mennään sinne,  tulee ylhäältä paalikossta Python Debugger. Mennään sinne
ja valitaan Django Launch and debug a Django web application. Vaihdetaan =>

{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django runserver",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}\\manage.py",
            "args": [
                "runserver"
            ],
            "django": true,
            "justMyCode": false
        }
    ]
}

Etsiminen/filtroiminen adminissa, kysely/admin.py:ssa:


from django.contrib import admin

from .models import Kysymys, Vaihtoehto

class VastausvaihtoehtoInline(admin.TabularInline):
    model = Vaihtoehto
    extra = 3


@admin.register(Kysymys)
class KysymysAdmin(admin.ModelAdmin):
    # date_hierarchy = "julkaisupvm"
    fieldsets = [
        ("Päivämäärätiedot", {"fields": ["julkaisupvm"]}),
        ("Sisältö", {"fields": ["teksti"]}),
    ]
    inlines = [VastausvaihtoehtoInline]
    list_display = ["teksti", "julkaisupvm", "onko_julkaistu_lähiaikoina"]
    search_fields = ["teksti"] # search_fields = ["question_text"]  => question_text => vaihdettu tekstiksi

@admin.register(Vaihtoehto)
class VaihtoehtoAdmin(admin.ModelAdmin):
    list_display = ["kysymys", "teksti"]
    # Voidaan lisätä "Vaihtoehdolle" myös 
    search_fields = ["teksti"] # Tai search_fields = ["teksti", "kysymys__teksti"]  kun lisätään "kysymys__teksti", se etsii kysymys kentältä. Huom! kaksi alaviiva.
Jos katsotaan modelia klikkamalla Ctrl ja Vaihtoehto, mennään model.py:n. Siellä nähdään 
kysymys = models.ForeignKey(Kysymys, on_delete=models.CASCADE)
Kysymys viittää toisen modeliin ForeignKey:lla. Tietokannassa Kysymys on id numerona. Emme voi suoraan käyttää id numerolla hakukentällä, koska se on vaan numero. Jos halutaan kysymys teksteinä, pitää sanoa Django:lle numeron kautta pitää etsiä tekstit. Siihen toimii Djangossa kahden alaviivaa merkintötapa.

Django admin sivuttain näyttää oletuksena 100 kerrallaan. Django sivussa linkki miten pystyy vaihtamaan sitä. Sinne pystyy lisäämään list_per_page

from django.contrib import admin

from .models import Kysymys, Vaihtoehto

class VastausvaihtoehtoInline(admin.TabularInline):
    model = Vaihtoehto
    extra = 3


@admin.register(Kysymys)
class KysymysAdmin(admin.ModelAdmin):
    # date_hierarchy = "julkaisupvm"
    fieldsets = [
        ("Päivämäärätiedot", {"fields": ["julkaisupvm"]}),
        ("Sisältö", {"fields": ["teksti"]}),
    ]
    inlines = [VastausvaihtoehtoInline]
    list_display = ["teksti", "julkaisupvm", "onko_julkaistu_lähiaikoina"]
    search_fields = ["teksti"]
    list_per_page = 4

@admin.register(Vaihtoehto)
class VaihtoehtoAdmin(admin.ModelAdmin):
    list_display = ["kysymys", "teksti"]
    search_fields = ["teksti", "kysymys__teksti"]
    list_per_page = 6  # kuinka monta sivua voidaan näyttää 
    list_max_show_all = 8 # voidaan rajoittaa max sivut määrämällä


Tulee ongelma Django adminissa, jos siellä on viittauksen toiseen modeliin, esim.muokkaa vaihtoehto sivulla, Kysymys kentää viitää Kysymys modelin. Oletuksena renderoi kaikki kysymyksiä mitkä tietokannassa on. Jos ajatellaan, ettää käyttäjät vaikka 10 000 ja käyttävät kenta, siellä voisi olla todella paljon kysymyksia ja lataaminen vie hirveä paljon aika. Sinne on ratkaisu miten voi estää:

https://docs.djangoproject.com/en/5.0/ref/contrib/admin/
Siellä pitää olla search_fields määritelty.
______________________________________
Huom! Djangon versio
class QuestionAdmin(admin.ModelAdmin):
    ordering = ["date_created"]
    search_fields = ["question_text"]
class ChoiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ["question"] # Pitää lisätä
_________________________________________



from django.contrib import admin

from .models import Kysymys, Vaihtoehto

class VastausvaihtoehtoInline(admin.TabularInline):
    model = Vaihtoehto
    extra = 3


@admin.register(Kysymys)
class KysymysAdmin(admin.ModelAdmin):
    # date_hierarchy = "julkaisupvm"
    fieldsets = [
        ("Päivämäärätiedot", {"fields": ["julkaisupvm"]}),
        ("Sisältö", {"fields": ["teksti"]}),
    ]
    inlines = [VastausvaihtoehtoInline]
    list_display = ["teksti", "julkaisupvm", "onko_julkaistu_lähiaikoina"]
    search_fields = ["teksti"]
    list_per_page = 4

@admin.register(Vaihtoehto)
class VaihtoehtoAdmin(admin.ModelAdmin):
    list_display = ["kysymys", "teksti"]
    search_fields = ["teksti", "kysymys__teksti"]
    list_per_page = 6  
    list_max_show_all = 8 
    autocomplete_fields = ["kysymys"] # Tulee ladattua aika nopeasti!!!!

Voidaaan lisätä consoliin muutamia kysymyksiä.
python manage.py shell
In [3]: from kysely.models import Kysymys

Kysymys.objects.all()
 # Otetaan joku teksti
text = """
joku teksti
"""
In [7]: sanat = text.split()

In [8]: import random
In [9]: random.choice(sanat)

In [10]: ' '.join([random.choice(sanat) for x in range (random.randint(4, 7))])
In [11]: def satunainen_lause(): return ' '.join([random.choice(sanat) for x in range (random.randint(4, 7))])

In [23]: kysymykset =[Kysymys(teksti=satunainen_lause() + "?", julkaisupvm= "2024-01-01T00:00:00+02:00") for i in range(1000)]
In [24]: len(kysymykset)
Out[24]: 1000

In [25]: kysymykset[4]
In [29]: Kysymys.objects.bulk_create(kysymykset)
#Voidaan katsoa kuinka monta kysymyksiä tietokannassa 
In [30]: Kysymys.objects.count()

Konsolin lisätään 10 vuoden päivämäärät 

from kysely.models import Kysymys
In [4]: Kysymus.objects.filter(julkaisupvm="2024-01-01T00:00:00+02:00").count()
In [6]: k=Kysymys.objects.filter(julkaisupvm="2024-01-01T00:00:00+02:00")
In [7]: k.count()
In [9]: k[0].julkaisupvm
Out[9]: datetime.datetime(2023, 12, 31, 22, 0, tzinfo=datetime.timezone.utc)
n [10]: d=k[0].julkaisupvm
In [11]: from datetime import timedelta
In [12]: import random
In [16]: for x in k:
    ...:     x.julkaisupvm = d-timedelta(seconds=random.randint(60*60*24*365, 10*60*60*24*365))
    ...:
In [17]: Kysymys.objects.bulk_update(k, ["julkaisupvm"])
Out[17]: 1115

In [18]: k[5].julkaisupvm
Out[18]: datetime.datetime(2014, 9, 5, 22, 40, 58, tzinfo=datetime.timezone.utc)


https://medium.com/@franciscovcbm/infinite-scroll-with-django-and-htmx-27f61cfaf911 voidaan katsoa oppimaan syvemmin

Voidaan vaihtaa/ylikirjoittaa django admin:n sivu omalla tavalla.Tassa esimerkki miten voidaan vaihtaa etupääotsikko

venv=> lib/python3.10/site-packages => django => contrib => admin => templates => admin => base_site.html sieltä otetaan copy ja paste sivusto/templates alle admin/base_site.html tiedosto:


{% extends "admin/base.html" %}

{% block title %}{% if subtitle %}{{ subtitle }} | {% endif %}{{ title }} | {{ site_title|default:_('Django site admin') }}{% endblock %}

{% block branding %}
<div id="site-name"><a href="{% url 'admin:index' %}">{{ site_header|default:_('Django administration') }}</a></div> # HUom!!! Täässä vaihdettu {{ site_header|default:_('Django administration') }} => Kyselyiden hallinta:ksi.
{% if user.is_anonymous %}
  {% include "admin/color_theme_toggle.html" %}
{% endif %}
{% endblock %}

{% block nav-global %}{% endblock %}


Voidaan instaloida Django_Debug_Toolbar

pip install django-debug-toolbar
Pitää tarkistaa onko settings.py :ssa INSTALLED_APPS:ssa 'django.contrib.staticfiles', asennettuna
ja TEMPLATES:ssa varmistaa
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        # ...
    }
]

ja pitää lisätä INSTALLED_APPS:in 

INSTALLED_APPS = [
    # ...
    "debug_toolbar",
    # ...
]

ja pitää lisätä URLs:in 

from django.urls import include, path

urlpatterns = [
    # ...
    path("__debug__/", include("debug_toolbar.urls")),
]

Sitten lisäätään:
MIDDLEWARE = [
    # ...
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ...
]

Sitten lisätään:

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


templates\kysely:n sisällä olevien html tiedostoihin lisätään 
<html>
<body>
# ...
</html>
</body>

Voidaan lisätä requirments.txt. Se on yleensä semmonen teidosto, mistä pip insall packet:t asentaa. 
pip freeze > requirements.txt
ja erilla tavalla:
pip install pip-tools
Ja luodaan uusi tiedosto
requirements.in
django
django-debug-toolbar

ja ajetaan 
pip-compile

Se lukee requirements.in tiedoston ja luo sen perusteella uuden requirements.txt

Jos lisätään 
ipython  => requirements.in tiedostoon
pip-tools  => requirements.in tiedostoon
pitää ajaa uudestaan pip-compile

kun ajetaan 
pip install -r requirements.txt täällä tavalla pystyy asentamaan kaikki paketit, mitä requirements.txt:ssa on 

Tehdään base.html => templates\kysely:n
Voidaan periytää 
{% load static %}
<html>
<body>
<head>
<link rel="stylesheet" href="{% static 'kysely/style.css' %}">

{% block content %}
{% end block %}
</head>
</body>
</html>

Ja muutetaan muita html tiedostoja lisäämällä 

{% extends 'kysely/base.html' %}

Otetaan {% load static %} pois.

{% extends kysely/base.html %} ensimmäisenä rivinä

Ja otetaan pois

<html>
<body>
<head>
<link rel="stylesheet" href="{% static 'kysely/style.css' %}">

</head>
</body>
</html>

Ja html sisältö laitetaan 

{% block content %}
Huom!sisältö tänne
{% end block %}


Eli esimerkiksi index.html:


{% extends 'kysely/base.html' %}

{% block content %}

{% if kysymykset %}
    <ul>
    {% for kysym in kysymykset %}
        <li><a href="{% url 'kysely:näytä' kysym.id %}">{{ kysym.teksti }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>Ei kyselyitä saatavilla.</p>
{% endif %}
{% endblock %}




Tässä muutamia linkkija vaihtamaan django admin:n:

https://github.com/sehmaschine/django-grappelli //vaihtaa admin sivua

https://github.com/pennersr/django-allauth // lisää facebook tai google kirjautumisen 















    


























-->
