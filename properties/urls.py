from django.urls import path
from properties import views

urlpatterns = [
    path('', views.PropertyListView.as_view(), name='property-list'),
    path('<int:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
]
