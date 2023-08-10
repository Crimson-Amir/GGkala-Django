from django.urls import path
from .views import DeleteReview

urlpatterns = [
    # path('rate/', NewReview, name='rate'),
    path('delete-review/<int:pk>/', DeleteReview.as_view(), name='delete_review')
]