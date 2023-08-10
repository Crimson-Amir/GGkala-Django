from django.urls import path
from . import views

app_name = "Home"

urlpatterns = [
    path('', views.home_page, name='home'),
    path('publisher/<slug:publisher>/', views.PublisherList.as_view(), name='publisher_url'),
]
