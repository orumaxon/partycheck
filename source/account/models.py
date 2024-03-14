from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email'), blank=True, null=True)
    patronymic = models.CharField(_('patronymic'), max_length=150, blank=True)

    REQUIRED_FIELDS = []

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

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
