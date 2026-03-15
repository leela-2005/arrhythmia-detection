from django.urls import path
from .views import blockchain_view

urlpatterns = [
    path('', blockchain_view, name='blockchain'),
]
