from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from .forms import (
    DebtCreateForm, PartyCreateForm, PaymentCreateForm,
    PartyUpdateForm, TransactionCreateForm,
)
from .models import Party, Payment, Transaction, Debt
from common.views.mixins import SigninRequiredMixin


class PartyListView(SigninRequiredMixin, generic.ListView):
    model = Party
    template_name = 'party/list.html'
    ordering = 'id'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(
            Q(creator=self.request.user) | Q(members__in={self.request.user})
        ).distinct()
        return super().get_queryset()


class PartyDetailView(SigninRequiredMixin, generic.DetailView):
    model = Party
    template_name = 'party/detail.html'

    def dispatch(self, request, *args, **kwargs):
        object_id = kwargs[self.pk_url_kwarg]
        if object_id not in request.user.members_parties.values_list('id', flat=True):
            return redirect('party:list')
        return super(PartyDetailView, self).dispatch(request, *args, **kwargs)


class PartyCreateView(SigninRequiredMixin, generic.CreateView):
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


class PartyUpdateView(SigninRequiredMixin, generic.UpdateView):
    model = Party
    form_class = PartyUpdateForm
    template_name = 'party/update.html'

    def get_success_url(self):
        return reverse('party:detail', kwargs=self.kwargs)

    def form_valid(self, form):
        form.full_clean()
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class PaymentCreateView(SigninRequiredMixin, generic.CreateView):
    model = Payment
    form_class = PaymentCreateForm
    template_name = 'party/add_payment.html'

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
        self.object = form.save()

        on_all = form.cleaned_data.get('on_all')
        if on_all:
            members_count = self.object.party.members.count()
            debt_price = self.object.price // members_count
            debts = [
                Debt(
                    payment=self.object,
                    debtor=member,
                    price=debt_price,
                )
                for member in self.object.party.members.all()
            ]
            Debt.objects.bulk_create(debts)

        return HttpResponseRedirect(self.get_success_url())


class DebtCreateView(SigninRequiredMixin, generic.CreateView):
    model = Debt
    form_class = DebtCreateForm
    template_name = 'party/add_debt.html'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update(dict(party_id=self.kwargs[self.pk_url_kwarg]))
        return form_kwargs

    def get_success_url(self):
        self.kwargs.pop('payment_id')
        return reverse('party:detail', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_id'] = self.kwargs[self.pk_url_kwarg]
        return context

    def form_valid(self, form):
        form.instance.payment_id = self.kwargs['payment_id']
        form.instance.debtor = self.request.user
        form.full_clean()
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class TransactionCreateView(SigninRequiredMixin, generic.CreateView):
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
