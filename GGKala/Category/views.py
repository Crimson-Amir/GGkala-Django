from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category
from Products.models import SexToys, Feature, ProductFeature
from django.db.models import Count, Avg
from django.db.models import Min, Max


class MainListView(ListView):
    template_name = 'Category/sextoys_list.html'
    queryset = SexToys.object.return_published_product()


class CategoryListView(ListView):
    paginate_by = 28
    template_name = 'category/sex_toys_slug.html'

    def get_queryset(self):
        slug = self.kwargs.get('slugname')
        category = get_object_or_404(Category.objects.return_truestatus(), slug=slug)
        brands = self.request.GET.getlist('brand')
        colors = self.request.GET.getlist('color')
        sorted_by = self.request.GET.get('sorted-by')
        toys_size = self.request.GET.getlist('toys_size')
        toys_score = self.request.GET.getlist('score')
        price_start = self.request.GET.get('ra-st')
        price_end = self.request.GET.get('ra-en')

        global queryset
        queryset = category.sexy_toys_related_name.return_published_product()

        for featur in category.features.all():
            # name = featur.feature_slug.replace('-', '_')
            # setattr(self, name,
            if self.request.GET.getlist(featur.feature_slug):
                queryset = queryset.filter(product_features__product_feature_slug__in=self.request.GET.getlist(featur.feature_slug))

        sort_options = {
            "score": queryset.annotate(res_off=Avg('review__rate')).order_by('-res_off'),
            "newst": queryset.order_by('-id'),
            "price-down": queryset.order_by('real'),
            "price-up": queryset.order_by('-real')
        }
        queryset = sort_options.get(sorted_by, queryset.annotate(res_off=Count('hits')).order_by('-res_off'))

        if brands:
            queryset = queryset.filter(brand__brand_name__in=brands)
        if colors:
            queryset = queryset.filter(color__slug__in=colors)

        if price_start and price_end:
            queryset = queryset.filter(real__range=(int(price_start), int(price_end)))

        if toys_score:
            queryset = queryset.annotate(res_off=Avg('review__rate')).filter(res_off__in=toys_score)

        if 'didlo' in slug:
            if toys_size:
                size_ranges = []
                for size_range_str in toys_size:
                    size_range_split = size_range_str.split('to')
                    size_range = range(int(size_range_split[0]), int(size_range_split[1]) + 1)
                    size_ranges.extend(size_range)
                queryset = queryset.filter(size__in=size_ranges)

        global product_count
        product_count = queryset.count()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slugname')
        category = get_object_or_404(Category.objects.return_truestatus(), slug=slug)
        wo_change = category.sexy_toys_related_name.return_published_product()

        context['features'] = category.features.all()
        context['url_keys'] = list(self.request.GET.keys())
        context['url_keys_len'] = len(list(self.request.GET.keys()))
        context['queryset'] = wo_change
        context['cat'] = category
        context['val'] = self.request.GET.get('sorted-by')
        context['brands'] = self.request.GET.getlist('brand')
        context['colors'] = self.request.GET.getlist('color')
        context['url'] = self.request.get_full_path()
        context['query_string'] = self.request.META.get('QUERY_STRING', '')
        context['product_count'] = product_count
        context['toys_size'] = self.request.GET.getlist('toys_size')
        context['toys_score'] = self.request.GET.getlist('score')
        context['categories'] = Category.objects.published_categories().annotate(product_count=Count('id')).order_by('-product_count')
        context['unique_colors'] = wo_change.values('color__color_name', 'color__slug', 'color__color_rgb', 'color__id').annotate(product_count=Count('id')).order_by('-product_count')
        context['price_start'] = self.request.GET.get('ra-st')
        context['price_end'] = self.request.GET.get('ra-en')
        context['min_price'] = category.sexy_toys_related_name.return_published_product().aggregate(Min('real'), Max('real'))
        context['unique_brands'] = wo_change.values('brand__brand_name', 'brand__id').annotate(product_count=Count('id')).order_by('-product_count')

        # context['filter_name'] = filter_name
        # context['filter_values'] = filter_values
        return context
