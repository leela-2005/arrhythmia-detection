from django.urls import path
from .views import dashboard_view, home_view, visualize_view, visualize_subject_view
from . import views

urlpatterns = [
    path('', home_view, name='home'),
    path('analysis/result/', dashboard_view, name='dashboard'), # moved dashboard to specific url
    path('visualize/', visualize_view, name='visualize'),
    path('visualize/<str:subject_id>/', visualize_subject_view, name='visualize_subject'),
    path('blockchain-records/', views.blockchain_records_view, name='blockchain_records'),
    path('verify-record/<int:record_id>/', views.verify_record, name='verify_record'),
]
