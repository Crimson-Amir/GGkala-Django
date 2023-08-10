from django.urls import path
from . import views

app_name = 'Products'

urlpatterns = [
    path('<slug:slugname>/', views.detail, name='detail'),
    path('preview/<int:pk>/', views.DetailPreview.as_view(), name='preview'),
]