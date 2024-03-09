from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (
    PartyDetailView, PartyListView, PartyCreateView,
    PaymentCreateView, PartyUpdateView, TransactionCreateView
)

app_name = 'party'
urlpatterns = [
    path('', login_required(PartyListView.as_view()), name='list'),
    path('create/', login_required(PartyCreateView.as_view()), name='create'),
    path('<int:pk>/', login_required(PartyDetailView.as_view()), name='detail'),
    path('<int:pk>/update/', login_required(PartyUpdateView.as_view()), name='update'),
    path('<int:pk>/add-payment/', login_required(PaymentCreateView.as_view()), name='add_payment'),
    path('<int:pk>/add-transaction/', login_required(TransactionCreateView.as_view()), name='add_transaction'),
]
