from django.urls import path

from .views import PartyDetailView, PartyListView

app_name = 'party'
urlpatterns = [
    path('<int:pk>/', PartyDetailView.as_view(), name='detail'),
    # path('payment/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),

    path('', PartyListView.as_view(), name='parties'),
]
