from django.db import models

from account.models import User
from common.models.mixins import CreatedAtMixin


class Party(CreatedAtMixin, models.Model):
    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    name = models.CharField(verbose_name='Наименование', max_length=150)
    creator = models.ForeignKey(
        User, models.PROTECT, verbose_name='Создатель', related_name='parties')
    members = models.ManyToManyField(User, verbose_name='Участники', blank=True, related_name='members_parties')

    def __str__(self):
        return f'#{self.id} Компания: {self.name}'

    def get_debts(self):
        debts_data = dict()

        for member in self.members.all():
            sum_d = 0

            member_debts = (
                member.debts.select_related('payment__sponsor')
                .filter(payment__party_id=self.id)
                .exclude(payment__sponsor_id=member.id)
            )
            for debt in member_debts:
                sum_d += debt.price
                key = (member, debt.payment.sponsor)
                debts_data[key] = debts_data.get(key, 0) + debt.price

            member_transactions = (
                member.sender_transactions.select_related('recipient')
                .filter(party=self.id)
            )
            for transaction in member_transactions:
                sum_d -= transaction.value
                key = (member, transaction.recipient)
                debts_data[key] = debts_data.get(key, 0) - transaction.value

            # print(f'Сам должен всего: {sum_d}')
            # print(f'Кому должен: {debts_data}')

        return debts_data

    def get_debt_by_members(self):
        debt_list_ = []

        # ToDo: оптимизировать запросы
        for member in self.members.all():

            sum_p = member.sponsor_payments.filter(party=self.id). \
                aggregate(models.Sum('price'))['price__sum'] or 0
            # print(f'Потратил: {sum_p}')

            sum_d = member.debts.filter(payment__party_id=self.id). \
                aggregate(models.Sum('price'))['price__sum'] or 0
            # print(f'Должен: {sum_d}')

            sum_st = member.sender_transactions.filter(party=self.id). \
                 aggregate(models.Sum('value'))['value__sum'] or 0
            # print(f'Отдал: {sum_st}')

            sum_rt = member.recipient_transactions.filter(party=self.id). \
                 aggregate(models.Sum('value'))['value__sum'] or 0
            # print(f'Получил: {sum_rt}')

            sum_ = sum_p - sum_d + sum_st - sum_rt
            debt_list_.append((member, sum_))
            # print(f'Итог: {sum_}')

        return debt_list_


class Payment(CreatedAtMixin, models.Model):
    class Meta:
        verbose_name = 'Расход в компании'
        verbose_name_plural = 'Расходы в компании'

    party = models.ForeignKey(
        Party, models.CASCADE, verbose_name='Компания', related_name='payments')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    sponsor = models.ForeignKey(
        User, models.PROTECT, verbose_name='Кто платил', related_name='sponsor_payments')
    price = models.FloatField(verbose_name='Сумма расхода')
    py_debtors = models.ManyToManyField(
        User, verbose_name='На кого делить расходы', related_name='debtors_payments')
    comment = models.CharField(verbose_name='Комментарий', max_length=300, blank=True, null=True)

    def __str__(self):
        return f'#{self.id} Расход: {self.sponsor} на сумму {self.price}'

    def get_debt_value(self):
        return self.price // self.party.members.count()

    def get_unknown_debt_price(self):
        known_debt = self.debts.aggregate(models.Sum('price'))['price__sum'] or 0
        return self.price - known_debt


class Debt(models.Model):
    class Meta:
        verbose_name = 'Долг'
        verbose_name_plural = 'Долги'

    payment = models.ForeignKey(
        Payment, models.CASCADE, verbose_name='Расход', related_name='debts')
    debtor = models.ForeignKey(
        User, models.PROTECT, verbose_name='Должник', related_name='debts')
    price = models.FloatField(verbose_name='Сумма')
    comment = models.CharField(verbose_name='Комментарий', max_length=300, blank=True, null=True)

    def __str__(self):
        return f'#{self.id} {self.debtor} должен {self.price} в Расходе #{self.payment_id}'


class Transaction(CreatedAtMixin, models.Model):
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    party = models.ForeignKey(
        Party, models.CASCADE, verbose_name='Компания/группа', related_name='transactions')
    sender = models.ForeignKey(
        User, models.PROTECT, verbose_name='Отправитель', related_name='sender_transactions')
    recipient = models.ForeignKey(
        User, models.PROTECT, verbose_name='Получатель', related_name='recipient_transactions')
    value = models.FloatField(verbose_name='Сумма перевода')
    comment = models.CharField(verbose_name='Краткий комментарий', max_length=300, blank=True, null=True)

    def __str__(self):
        return f'#{self.id} Перевод: {self.sender} -> {self.recipient}: {self.value}'
