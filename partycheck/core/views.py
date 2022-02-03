from django.views import generic

from core.models import PartyGroup


class GroupDetailView(generic.DetailView):
    model = PartyGroup
    template_name = 'core/group.html'


# class PaymentDetailView(generic.DetailView):
#     model = PartyGroup
#     template_name = 'core/group.html'
