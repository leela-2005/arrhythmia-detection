from django.urls import path
from ecg.views import upload_ecg


urlpatterns = [
    path('process/<str:record_name>/', process_ecg),
    path('upload/', upload_ecg),
]
