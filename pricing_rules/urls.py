from django.urls import path
from pricing_rules import views

urlpatterns = [
    path('', views.PricingRuleListView.as_view(), name='pricing-rule-list'),
    path('<int:pk>/', views.PricingRuleDetailView.as_view(), name='pricing-rule-detail'),
]
