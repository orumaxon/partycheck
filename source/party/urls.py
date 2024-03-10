from django.urls import path

from .views import (
    PartyDetailView, PartyListView, PartyCreateView,
    PaymentCreateView, PartyUpdateView, TransactionCreateView
)

app_name = 'party'
urlpatterns = [
    path('', PartyListView.as_view(), name='list'),
    path('create/', PartyCreateView.as_view(), name='create'),
    path('<int:pk>/', PartyDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', PartyUpdateView.as_view(), name='update'),
    path('<int:pk>/add-payment/', PaymentCreateView.as_view(), name='add_payment'),
    path('<int:pk>/add-transaction/', TransactionCreateView.as_view(), name='add_transaction'),
]
