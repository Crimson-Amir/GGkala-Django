from django.urls import path
from . import views

app_name = 'Category'

urlpatterns = [
    path('', views.MainListView.as_view(), name='sex_toys'),
    path('<slug:slugname>/', views.CategoryListView.as_view(), name='sex_toys_slug'),
]