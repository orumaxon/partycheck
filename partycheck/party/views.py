from django.db.models import Q
from django.views import generic

from party.models import Party


class PartyDetailView(generic.DetailView):
    model = Party
    template_name = 'party/party.html'


class PaymentDetailView(generic.DetailView):
    model = Party
    template_name = 'party/party.html'


class PartyListView(generic.ListView):
    model = Party
    template_name = 'party/parties.html'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(
            Q(creator=self.request.user) | Q(members__in={self.request.user})
        ).distinct()
        return super().get_queryset()
