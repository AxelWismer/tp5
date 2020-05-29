from django.urls import path
from .views import Montecarlo, Montecarlo2
app_name = 'montecarlo'

urlpatterns = [
    path('product1/', Montecarlo.as_view(), name='montecarlo'),
    path('product2/', Montecarlo2.as_view(), name='montecarlo2'),
]
