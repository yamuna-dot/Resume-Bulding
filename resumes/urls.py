from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create/', views.resume_create_view, name='resume_create'),
    path('<int:pk>/preview/', views.resume_preview_view, name='resume_preview'),
    path('<int:pk>/edit/', views.resume_edit_view, name='resume_edit'),
    path('<int:pk>/delete/', views.resume_delete_view, name='resume_delete'),
    path('<int:pk>/pdf/', views.resume_download_pdf_view, name='resume_pdf'),
]
