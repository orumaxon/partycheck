from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import PartyDetailView, PartyListView, PartyCreateView

app_name = 'party'
urlpatterns = [
    path('<int:pk>/', login_required(PartyDetailView.as_view()), name='detail'),
    path('create/', login_required(PartyCreateView.as_view()), name='create'),
    path('', PartyListView.as_view(), name='parties'),
]
