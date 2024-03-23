from django.db.models import Prefetch, Sum, F
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from account.models import User
from common.views.mixins import CacheMixin, SigninRequiredMixin

from .forms import (
    DebtCreateForm, PartyCreateForm, PaymentCreateForm,
    PartyUpdateForm, TransactionCreateForm,
)
from .models import Party, Payment, Transaction, Debt


class PartyListView(SigninRequiredMixin, generic.ListView):
    model = Party
    template_name = 'party/list.html'
    ordering = 'id'

    def get_queryset(self):
        self.queryset = (
            self.request.user.members_parties.select_related('creator')
            .prefetch_related(Prefetch('members', queryset=User.objects.only('id', 'username')))
            .only('name', 'creator__id', 'creator__username')
        )
        return super().get_queryset()


class PartyDetailView(SigninRequiredMixin, generic.DetailView):
    model = Party
    template_name = 'party/detail.html'

    def get_queryset(self):
        prefetch_for_debts = (
            Debt.objects.select_related('debtor')
            .only('id', 'price', 'comment', 'debtor__id', 'debtor__username', 'payment__id')
        )
        prefetch_for_payments = (
            Payment.objects.select_related('sponsor')
            .prefetch_related(Prefetch('debts', queryset=prefetch_for_debts))
            .annotate(unknown_debt_price=Coalesce((F('price') - Sum('debts__price')), F('price')))
            .only('id', 'price', 'comment', 'sponsor__id', 'sponsor__username', 'party__id')
        )
        self.queryset = (
            self.model.objects
            .prefetch_related(Prefetch('payments', queryset=prefetch_for_payments))
            .prefetch_related('transactions', 'transactions__sender', 'transactions__recipient')
        )
        return super().get_queryset()

    def dispatch(self, request, *args, **kwargs):
        qs = (
            self.model.objects.prefetch_related('members')
            .filter(members__id=self.request.user.id)
        )
        if not qs.exists():
            return redirect('party:list')
        return super(PartyDetailView, self).dispatch(request, *args, **kwargs)


class PartyCreateView(SigninRequiredMixin, generic.CreateView):
    model = Party
    form_class = PartyCreateForm
    template_name = 'party/create.html'

    def get_success_url(self):
        return reverse('party:list', kwargs=self.kwargs)

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


class PaymentCreateView(SigninRequiredMixin, CacheMixin, generic.CreateView):
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

        cache_args = [self.kwargs[self.pk_url_kwarg], self.request.user.username]
        self.cache.clear('party_info', cache_args)
        return HttpResponseRedirect(self.get_success_url())


class DebtCreateView(SigninRequiredMixin, CacheMixin, generic.CreateView):
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

        cache_args = [self.kwargs[self.pk_url_kwarg], self.request.user.username]
        self.cache.clear('party_info', cache_args)
        return HttpResponseRedirect(self.get_success_url())


class DebtSendView(SigninRequiredMixin, CacheMixin, generic.View):
    pk_url_kwarg = "pk"

    def get(self, request, **kwargs):
        debt_id = self.kwargs.pop('debt_id')
        debt = Debt.objects.get(id=debt_id)
        Transaction.objects.create(
            party=debt.payment.party,
            sender=debt.debtor,
            recipient=debt.payment.sponsor,
            value=debt.price,
        )
        url = reverse('party:detail', kwargs=self.kwargs)

        cache_args = [self.kwargs[self.pk_url_kwarg], self.request.user.username]
        self.cache.clear('party_info', cache_args)
        return HttpResponseRedirect(url)


class TransactionCreateView(SigninRequiredMixin, CacheMixin, generic.CreateView):
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

        cache_args = [self.kwargs[self.pk_url_kwarg], self.request.user.username]
        self.cache.clear('party_info', cache_args)
        return HttpResponseRedirect(self.get_success_url())
