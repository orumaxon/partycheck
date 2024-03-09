from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from party.forms import (
    PartyCreateForm, PaymentCreateForm, PartyUpdateForm, TransactionCreateForm
)
from party.models import Party, Payment, Transaction


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
        object_id = kwargs[self.pk_url_kwarg]
        if object_id not in request.user.members_parties.values_list('id', flat=True):
            return redirect('party:list')
        return super(PartyDetailView, self).dispatch(request, *args, **kwargs)


class PartyCreateView(generic.CreateView):
    model = Party
    form_class = PartyCreateForm
    template_name = 'party/create.html'

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.full_clean()
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class PartyUpdateView(generic.UpdateView):
    model = Party
    form_class = PartyUpdateForm
    template_name = 'party/update.html'

    def get_success_url(self):
        return reverse('party:detail', kwargs=self.kwargs)

    def form_valid(self, form):
        form.full_clean()
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class PaymentCreateView(generic.CreateView):
    model = Payment
    form_class = PaymentCreateForm
    template_name = 'party/add_payment.html'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update(dict(
            party_id=self.kwargs[self.pk_url_kwarg],
        ))
        return form_kwargs

    def get_success_url(self):
        return reverse('party:detail', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_id'] = self.kwargs[self.pk_url_kwarg]
        return context

    def form_valid(self, form):
        form.instance.sponsor = self.request.user
        form.instance.party_id = self.kwargs[self.pk_url_kwarg]
        form.full_clean()
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class TransactionCreateView(generic.CreateView):
    model = Transaction
    form_class = TransactionCreateForm
    template_name = 'party/add_transaction.html'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update(dict(
            user=self.request.user,
            party_id=self.kwargs[self.pk_url_kwarg],
        ))
        return form_kwargs

    def get_success_url(self):
        return reverse('party:detail', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_id'] = self.kwargs[self.pk_url_kwarg]
        return context

    def form_valid(self, form):
        form.instance.party_id = self.kwargs[self.pk_url_kwarg]
        form.instance.sender = self.request.user
        form.full_clean()
        form.save()
        return HttpResponseRedirect(self.get_success_url())
