from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email'), blank=True, null=True)
    patronymic = models.CharField(_('patronymic'), max_length=150, blank=True)

    REQUIRED_FIELDS = []

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def get_payments_sum(self, party_id=None, exclude_self_debts=False):
        """Общая сумма потраченных средств пользователем"""
        filter_params = models.Q(party_id=party_id) if party_id else models.Q()
        sum_p = (
            self.sponsor_payments.filter(filter_params)
            .aggregate(models.Sum('price'))['price__sum']
        ) or 0

        if exclude_self_debts:
            filter_params = models.Q(payment__party_id=party_id) if party_id else models.Q()
            sum_p_self = (
                self.debts.filter(filter_params)
                .filter(payment__sponsor_id=self.id)
                .aggregate(models.Sum('price'))['price__sum']
            ) or 0
            sum_p -= sum_p_self

        # print(f'Потратил: {sum_p}')
        return sum_p

    def get_recipient_transactions_sum(self, party_id=None):
        """Общая сумма, которую вернули пользователю"""
        filter_params = models.Q(party_id=party_id) if party_id else models.Q()
        sum_rt = (
             self.recipient_transactions.filter(filter_params)
             .aggregate(models.Sum('value'))['value__sum']
         ) or 0

        # print(f'Получил: {sum_rt}')
        return sum_rt

    def get_debts_sum(self, party_id=None, exclude_self_sponsor=False):
        """Общая сумма долгов пользователя"""
        filter_params = models.Q(payment__party_id=party_id) if party_id else models.Q()
        exclude_params = models.Q(payment__sponsor_id=self.id) if exclude_self_sponsor else models.Q()

        sum_d = (
            self.debts.filter(filter_params).exclude(exclude_params)
            .aggregate(models.Sum('price'))['price__sum']
        ) or 0

        # print(f'Должен: {sum_d}')
        return sum_d

    def get_senders_transactions_sum(self, party_id=None):
        """Общая сумма, которую пользователь вернул"""
        filter_params = models.Q(party_id=party_id) if party_id else models.Q()
        sum_st = (
            self.sender_transactions.filter(filter_params)
            .aggregate(models.Sum('value'))['value__sum']
        ) or 0

        # print(f'Отдал: {sum_st}')
        return sum_st

    def get_full_debts(self):
        """Сколько должен сам пользователь"""
        return self.get_debts_sum(exclude_self_sponsor=True) - self.get_senders_transactions_sum()

    def get_full_payments(self):
        """Сколько должны пользователю"""
        return self.get_payments_sum(exclude_self_debts=True) - self.get_recipient_transactions_sum()

    def get_full_balance(self):
        # ToDo: deprecated
        print(self.id, self.username)

        sum_p = 0
        sum_pdata = dict()
        for pp in self.sponsor_payments.all():
            sum_p += pp.price
            for debtor in pp.py_debtors.exclude(id=self.id):
                sum_pdata[debtor.id] = sum_pdata.get(debtor.id, 0) + pp.get_debt_value()

        print(f'Потратил всего: {sum_p}')
        print(f'Кто должен: {sum_pdata}')

        sum_d = 0
        sum_ddata = dict()
        for pd in self.debtors_payments.exclude(sponsor__id=self.id):
            sum_d += pd.get_debt_value()
            sum_ddata[pd.sponsor.id] = pd.get_debt_value()

        print(f'Сам должен всего: {sum_d}')
        print(f'Кому должен: {sum_ddata}')

        return []
