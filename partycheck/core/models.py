from django.db import models

from account.models import User


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        abstract = True


class PartyGroup(CreatedAtMixin, models.Model):
    class Meta:
        verbose_name = 'Компания/группа'
        verbose_name_plural = 'Компании/группы'

    name = models.CharField(verbose_name='Наименование', max_length=150)
    creator = models.ForeignKey(
        User, models.SET_NULL,
        verbose_name='Создатель',
        null=True,
        related_name='party_groups',
    )
    members = models.ManyToManyField(
        User,
        verbose_name='Участники',
        blank=True,
        related_name='party_members',
    )

    def __str__(self):
        return f'#{self.id} Компания: {self.name}'

    def get_debt_by_user(self, user: User):
        """Получить общий долг должника компании"""
        sum_p = 0
        for pp in user.party_payments.filter(party_group=self):
            sum_p += pp.price
        print(f'Потратил: {sum_p}')

        sum_d = 0
        for pd in user.party_debtors.filter(party_group=self):
            sum_d += pd.get_debt_value()
        print(f'Должен: {sum_d}')

        sum_st = 0
        for pt in user.party_sender_transactions.filter(party_group=self):
            sum_st += pt.value
        print(f'Отдал: {sum_st}')

        sum_rt = 0
        for pt in user.party_recipient_transactions.filter(party_group=self):
            sum_rt += pt.value
        print(f'Получил: {sum_rt}')

        print(f'Итог: {sum_p - sum_d + sum_st - sum_rt}')


class PartyPayment(CreatedAtMixin, models.Model):
    class Meta:
        verbose_name = 'Расход на компанию'
        verbose_name_plural = 'Расходы на компанию'

    party_group = models.ForeignKey(
        PartyGroup, models.CASCADE,
        verbose_name='Компания/группа',
        related_name='party_payments',
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    investor = models.ForeignKey(
        User, models.SET_NULL,
        verbose_name='Кто платил',
        null=True,
        related_name='party_payments',
    )
    price = models.FloatField(verbose_name='Сумма расходов')
    debtors = models.ManyToManyField(
        User,
        verbose_name='На кого делить расходы',
        blank=True,
        related_name='party_debtors',
    )
    comment = models.CharField(verbose_name='Краткий комментарий', max_length=300, blank=True, null=True)

    def __str__(self):
        return f'#{self.id} Расход: {self.investor} на сумму {self.price}'

    def get_debt_value(self):
        return self.price // self.debtors.count()

    def get_ost_value(self):
        debt = self.get_debt_value()
        return self.price - debt * self.debtors.count()


class PartyTransaction(CreatedAtMixin, models.Model):
    class Meta:
        verbose_name = 'Денежный перевод между участниками компании'
        verbose_name_plural = 'Денежные переводы между участниками компании'

    party_group = models.ForeignKey(
        PartyGroup, models.CASCADE,
        verbose_name='Компания/группа',
        related_name='party_transactions',
    )
    sender = models.ForeignKey(
        User, models.SET_NULL,
        verbose_name='Отправитель',
        null=True,
        related_name='party_sender_transactions',
    )
    recipient = models.ForeignKey(
        User, models.SET_NULL,
        verbose_name='Получатель',
        null=True,
        related_name='party_recipient_transactions',
    )
    value = models.FloatField(verbose_name='Сумма перевода')
    comment = models.CharField(verbose_name='Краткий комментарий', max_length=300, blank=True, null=True)

    def __str__(self):
        return f'#{self.id} Перевод: {self.sender} - {self.recipient} ({self.value})'
