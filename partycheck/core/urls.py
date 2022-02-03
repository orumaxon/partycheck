from django.urls import path

from .views import GroupDetailView

app_name = 'party'
urlpatterns = [
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    # path('payment/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]
