from django.views import generic

from party.models import PartyGroup


class GroupDetailView(generic.DetailView):
    model = PartyGroup
    template_name = 'core/group.html'


# class PaymentDetailView(generic.DetailView):
#     model = PartyGroup
#     template_name = 'core/group.html'

class PartyListView(generic.ListView):
    model = PartyGroup
    template_name = 'core/party.html'
