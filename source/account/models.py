from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email'), blank=True, null=True)
    patronymic = models.CharField(_('patronymic'), max_length=150, blank=True)

    REQUIRED_FIELDS = []

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def get_debt_by_party(self, party):
        """Получить общий долг участника в компании"""
        sum_p = 0
        for pp in self.payments.filter(party=party):
            sum_p += pp.price
        # print(f'Потратил: {sum_p}')

        sum_d = 0
        for pd in self.debtors.filter(party=party):
            sum_d += pd.get_debt_value()
        # print(f'Должен: {sum_d}')

        sum_st = 0
        for pt in self.sender_transactions.filter(party=party):
            sum_st += pt.value
        # print(f'Отдал: {sum_st}')

        sum_rt = 0
        for pt in self.recipient_transactions.filter(party=party):
            sum_rt += pt.value
        # print(f'Получил: {sum_rt}')

        sum_ = sum_p - sum_d + sum_st - sum_rt
        # print(f'Итог: {sum_}')

        return sum_
