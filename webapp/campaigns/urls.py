from django.urls import path

from . import views

app_name = 'campaigns'
urlpatterns = [
    path('<int:campaign_id>/', views.Campaign.as_view(), name='campaign'),
    path('banner/<int:banner_id>/', views.banner, name='banner'),
]
