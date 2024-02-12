
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Kysymys


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
        self.assertIs(vanha_kysymys.onko_julkaistu_lähiaikoina, False)


    def test_onko_julkaistu_lähiaikoina_nykyisellä_kysymyksellä(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        vähimmän_kuin_vuorokausi = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        tuore_kysymys = Kysymys(julkaisupvm=vähimmän_kuin_vuorokausi)
        self.assertIs(tuore_kysymys.onko_julkaistu_lähiaikoina, True)
