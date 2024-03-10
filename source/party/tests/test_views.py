from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from account.models import User
from party.models import Party, Payment, Transaction

from .utils import create_party


class PartyListViewTestCase(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.user1 = User.objects.get(id=2)
        self.user2 = User.objects.get(id=3)
        self.user3 = User.objects.get(id=4)

    def test_get_page__anon_user__redirect_to_auth(self):
        response = self.client.get(reverse('party:list'))
        self.assertRedirects(response, '/account/signin/?next=/party/')

    def test_get_page__auth_user__ok(self):
        self.client.login(
            username=self.user1.username,
            password=self.user1.username,
        )
        response = self.client.get(reverse('party:list'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'party/list.html')
        self.assertEqual(response.context['user'].id, self.user1.id)

    def test_get_page__auth_user__return_parties(self):
        party1 = create_party(**dict(
            name='Party-1',
            creator=self.user1,
            members=[self.user1, self.user2],
        ))
        assert party1.creator.id == self.user1.id
        party_members_ids = list(party1.members.values_list('id', flat=True))
        assert party_members_ids == [self.user1.id, self.user2.id]

    def test__future(self):
        party1 = create_party(**dict(
            name='Party-1',
            creator=self.user1,
            members=[self.user1, self.user2, self.user3],
        ))
        a1 = Payment.objects.create(
            party=party1,
            sponsor=self.user1,
            price=1300,
        )
        a1.debtors.add(self.user1)
        a2 = Payment.objects.create(
            party=party1,
            sponsor=self.user1,
            price=300,
        )
        a2.debtors.add(self.user2)
        a3 = Payment.objects.create(
            party=party1,
            sponsor=self.user1,
            price=400,
        )
        a3.debtors.add(self.user3)

        party2 = create_party(**dict(
            name='Party-2',
            creator=self.user2,
            members=[self.user1, self.user2, self.user3],
        ))
        b1 = Payment.objects.create(
            party=party2,
            sponsor=self.user2,
            price=300,
        )
        b1.debtors.add(self.user2)
        b2 = Payment.objects.create(
            party=party2,
            sponsor=self.user2,
            price=500,
        )
        b2.debtors.add(self.user1)
        b3 = Payment.objects.create(
            party=party2,
            sponsor=self.user2,
            price=200,
        )
        b3.debtors.add(self.user3)

        self.user1.get_full_balance()
        print('-----')
        self.user2.get_full_balance()
        print('-----')
        self.user3.get_full_balance()
