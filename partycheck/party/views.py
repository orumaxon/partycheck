from django.db.models import Q
from django.shortcuts import redirect
from django.views import generic

from party.models import Party


class PartyDetailView(generic.DetailView):
    model = Party
    template_name = 'party/party.html'

    def dispatch(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        if object_id not in request.user.parties.values_list('id', flat=True):
            return redirect('party:parties')
        return super(PartyDetailView, self).dispatch(request, *args, **kwargs)


class PartyListView(generic.ListView):
    model = Party
    template_name = 'party/parties.html'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(
            Q(creator=self.request.user) | Q(members__in={self.request.user})
        ).distinct()
        return super().get_queryset()
