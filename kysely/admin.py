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
    # list_per_page = 4

@admin.register(Vaihtoehto)
class VaihtoehtoAdmin(admin.ModelAdmin):
    list_display = ["kysymys", "teksti"]
    search_fields = ["teksti", "kysymys__teksti"]
    # list_per_page = 6
    # list_max_show_all = 8
    autocomplete_fields = ["kysymys"]
    
