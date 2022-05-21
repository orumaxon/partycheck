from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import PartyDetailView, PartyListView, PartyCreateView, PaymentCreateView

app_name = 'party'
urlpatterns = [
    path('<int:pk>/', login_required(PartyDetailView.as_view()), name='detail'),
    path('<int:pk>/add-payment/', login_required(PaymentCreateView.as_view()), name='add_payment'),
    path('create/', login_required(PartyCreateView.as_view()), name='create'),
    path('', login_required(PartyListView.as_view()), name='parties'),
]
