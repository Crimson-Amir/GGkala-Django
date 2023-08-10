from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'status', "parent")
    list_filter = ('status',)
    search_fields = ('category_name', "slug")
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'slug', 'status', "parent")
    list_filter = ('status',)
    search_fields = ('brand_name', "slug")
    list_editable = ('status',)


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color_name', 'color_rgb', 'slug', 'status')
    list_filter = ('status',)
    search_fields = ('color_name', 'color_rgb', "slug")
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('color_name',)}