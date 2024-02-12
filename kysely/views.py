from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from .models import Kysymys, Vaihtoehto

    


class ListaNäkymä(generic.ListView):
    template_name = "kysely/indeksi.html"
    context_object_name = "kysymykset"

    def get_queryset(self):
        return Kysymys.objects.order_by("-julkaisupvm")[:2]


class NäytäNäkymä(generic.DetailView):
    model = Kysymys
    template_name = "kysely/näytä.html"


class TuloksetNäkymä(generic.DetailView):
    model = Kysymys
    template_name = "kysely/tulokset.html"


def äänestä(request, kysymys_id):
    kysym = get_object_or_404(Kysymys, pk=kysymys_id)
    try:
       valittu = kysym.vaihtoehto_set.get(pk=request.POST["valittu"])
    except (KeyError, Vaihtoehto.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "kysely/näytä.html",
            {
                "kysymys": kysym,
                "virheviesti": "Ei valittu.",
            },
        )
    else:
        valittu.ääniä += 1
        valittu.save()
        # Always return aion = get_objeRedirect atter successfully dealing
        # with PoST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("kysely:tulokset", args=(kysym.id,)))
    