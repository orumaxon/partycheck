from django.views import generic

from party.models import Party


class GroupDetailView(generic.DetailView):
    model = Party
    template_name = 'party/group.html'


class PaymentDetailView(generic.DetailView):
    model = Party
    template_name = 'party/group.html'


class PartyListView(generic.ListView):
    model = Party
    template_name = 'party/groups.html'
