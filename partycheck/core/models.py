from django.db import models

from account.models import User


class PartyGroup(models.Model):
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
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_created=True)
    members = models.ManyToManyField(User, verbose_name='Участники', blank=True)

    def __str__(self):
        return f'#{self.id} Компания: {self.name}'


class PartyPayment(models.Model):
    class Meta:
        verbose_name = 'Расход на компанию'
        verbose_name_plural = 'Расходы на компании'

    party_group = models.ForeignKey(
        PartyGroup, models.CASCADE,
        verbose_name='Компания/группа',
        related_name='party_payments',
    )
    investor = models.ForeignKey(
        User, models.SET_NULL,
        verbose_name='Кто платил',
        null=True,
        related_name='party_payments',
    )
    price = models.FloatField(verbose_name='Сумма расходов')
    debtors = models.ManyToManyField(User, verbose_name='На кого делить расходы', blank=True)
    comment = models.CharField(verbose_name='Краткий комментарий', max_length=300)

    def __str__(self):
        return f'#{self.id} Расход: {self.investor} на сумму {self.price}'


class PartyTransaction(models.Model):
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
    comment = models.CharField(verbose_name='Краткий комментарий', max_length=300)

    def __str__(self):
        return f'#{self.id} Перевод: {self.sender} - {self.recipient} ({self.value})'
