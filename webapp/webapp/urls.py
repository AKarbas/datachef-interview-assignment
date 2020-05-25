from django.urls import include, path

urlpatterns = [
    path('campaigns/', include('campaigns.urls')),
]
