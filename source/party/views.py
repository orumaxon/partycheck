from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic

from party.forms import PartyCreateForm, PaymentCreateForm
from party.models import Party, Payment


class PartyListView(generic.ListView):
    model = Party
    template_name = 'party/list.html'
    ordering = 'id'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(
            Q(creator=self.request.user) | Q(members__in={self.request.user})
        ).distinct()
        return super().get_queryset()


class PartyDetailView(generic.DetailView):
    model = Party
    template_name = 'party/detail.html'

    def dispatch(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        if object_id not in request.user.members.values_list('id', flat=True):
            return redirect('party:parties')
        return super(PartyDetailView, self).dispatch(request, *args, **kwargs)


class PartyCreateView(generic.CreateView):
    model = Party
    form_class = PartyCreateForm
    template_name = 'party/create.html'

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class PaymentCreateView(generic.CreateView):
    model = Payment
    form_class = PaymentCreateForm
    template_name = 'party/add_payment.html'

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        form.instance.sponsor = self.request.user
        form.instance.party_id = 12
        form.save()
        return HttpResponseRedirect(self.get_success_url())
