from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import PartyDetailView, PartyListView

app_name = 'party'
urlpatterns = [
    path('<int:id>/', login_required(PartyDetailView.as_view()), name='detail'),
    path('', PartyListView.as_view(), name='parties'),
]
