from django.contrib import admin
from . import models


@admin.register(models.ReviewModel)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_slug', 'comment_short', 'comment_title', 'rate', "created_at")
