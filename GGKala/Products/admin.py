from django.contrib import admin
from .models import SexToys, Feature, ProductFeature, ProductImage
from . import models


@admin.register(SexToys)
class SexToysAdmin(admin.ModelAdmin):
    list_display = ('title_short', 'return_pic', 'slug', 'brand', 'inventory', "publish", 'publisher', 'created_short', "show_category")
    list_filter = ('inventory', 'brand')
    search_fields = ('title', 'about')
    list_editable = ('inventory', 'publish')
    prepopulated_fields = {'slug': ('title',)}
    actions = ["make_published", "un_published"]

    # def show_category(self, obj):
    #     return ", ".join([cat.category_name for cat in obj.category.return_truestatus()])

    @admin.action(description="Mark selected stories as published")
    def make_published(self, request, queryset):
        queryset.update(publish="published")

    @admin.action(description="Mark selected stories as unpublished")
    def un_published(self, request, queryset):
        queryset.update(publish="unpublished")


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')
    list_editable = ('category',)


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'feature', 'value')
    search_fields = ('product', 'value')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product', 'image')


# @admin.register(PeopleBuyAlso)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ('product', 'image')
#     search_fields = ('product', 'image')