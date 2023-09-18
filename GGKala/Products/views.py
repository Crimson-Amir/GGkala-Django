from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views.generic import DetailView
# from Category import models
from .models import SexToys, ProductImage, Cart
from Category.models import Category
from account.mixin import PreviewMixin
from review.forms import ReviewForms
from review.models import ReviewModel
from django.db.models import Count, Avg, Q


def detail(request, slugname):
    mod = get_object_or_404(SexToys.object.return_published_product(), slug=slugname)
    same_products = mod.buy_also.all()
    products = ProductImage.objects.filter(product=mod)

    ip = request.user.ip_address
    if ip not in mod.hits.all():
        mod.hits.add(ip)

    if request.method == "POST":

        form = ReviewForms(request.POST)
        if form.is_valid():
            user = request.user
            clean_data = form.cleaned_data
            rating = request.POST.get('rate')
            prod_id = request.POST.get('product-id')
            product = SexToys.object.get(id=prod_id).slug
            r = ReviewModel.objects.create(user=user, product_slug=product, comment_title=clean_data['comment_title'], comment_body=clean_data['comment_body'], rate=rating)
            mod.review.add(r)
            return redirect('Products:detail', product)
    else:
        form = ReviewForms()

    p = mod.price - mod.discounted_price()
    return render(request, 'Products/detail_page.html', context={'object': mod, 'form': form, 'pictures': products,
                                                                 'first_color': mod.color.first, 'p': p, 'also_like': same_products})


def refresh_buy_also(requests, category_slug):
    products = get_object_or_404(Category.objects.return_truestatus(), slug=category_slug)
    sex_toys = products.sexy_toys_related_name.return_published_product().prefetch_related('carts')

    for mod in sex_toys:
        same_products = Cart.objects.filter(id__in=mod.carts.values('id')).values('all_product__id').annotate(product_count=Count('id')).order_by('-product_count')

        if not same_products:
            continue

        same_products = [d for d in same_products if d['all_product__id'] != mod.id]
        mod.buy_also.clear()
        related_products = [sex_toys.get(id=same['all_product__id']) for same in same_products[:5]]
        mod.buy_also.set(related_products)

    return HttpResponse('ok')


class DetailPreview(PreviewMixin, DetailView):
    template_name = 'Products/detail_page.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(SexToys, pk=pk)
