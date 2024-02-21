from django.contrib import admin

from .models import Kysymys, Vaihtoehto
 


@admin.register(Kysymys)
class KysymysAdmin(admin.ModelAdmin):
    fields = ["julkaisupvm", "teksti"]




@admin.register(Vaihtoehto)
class VaihtoehtoAdmin(admin.ModelAdmin):
    list_display = ["kysymys", "teksti"]




