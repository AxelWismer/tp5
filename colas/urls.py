from django.urls import path
from .views import Colas

app_name = 'colas'
urlpatterns = [
    path('', Colas.as_view(), name='colas'),
]
