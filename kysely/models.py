from django.db import models


class Kysymys(models.Model):
    teksti = models.CharField(max_length=200)
    julkaisupvm = models.DateTimeField("julkaistu")

    def __str__(self):
        return self.teksti

    class Meta():
        verbose_name="kysymys"
        verbose_name_plural="kysymykset"



class Vaihtoehto(models.Model):
    kysymys = models.ForeignKey(Kysymys, on_delete=models.CASCADE)
    teksti = models.CharField(max_length=200)
    ääniä = models.IntegerField(default=0)

    def __str__(self):
        return self.teksti

    class Meta():
        verbose_name="vaihtoehto"
        verbose_name_plural="vaihtoehdot"