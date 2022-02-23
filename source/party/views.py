from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic

from party.forms import PartyCreateForm
from party.models import Party


class PartyListView(generic.ListView):
    model = Party
    template_name = 'party/parties.html'
    ordering = 'id'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(
            Q(creator=self.request.user) | Q(members__in={self.request.user})
        ).distinct()
        return super().get_queryset()


class PartyDetailView(generic.DetailView):
    model = Party
    template_name = 'party/party.html'

    def dispatch(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        if object_id not in request.user.members.values_list('id', flat=True):
            return redirect('party:parties')
        return super(PartyDetailView, self).dispatch(request, *args, **kwargs)


class PartyCreateView(generic.CreateView):
    model = Party
    form_class = PartyCreateForm
    template_name = 'party/party_create.html'

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())
