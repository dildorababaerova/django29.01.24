from django.urls import reverse
from django.utils import timezone
import datetime
from django.test import TestCase
from ..models import Kysymys


def luo_kysymys(teksti, days):
    """
    Create a kysymys with the given `teksti` and published the
    given number of `days` offset to now (negative for kysymyss published
    in the past, positive for kysymyss that have yet to be published).
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
        Kysymys with a pub_date in the past are displayed on the
        indeksi page.
        """
        kysymys = luo_kysymys(teksti="Mennyt kysymys.", days=-30)
        vastaus = self.client.get(reverse("kysely:indeksi"))
        self.assertQuerySetEqual(
            vastaus.context["kysymykset"],
            [kysymys],
        )

    def test_tuleva_kysymys(self):
        """
        Kysymysk pub_date in the future aren't displayed on
        the indeksi page.
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