from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views.generic import DetailView
# from Category import models
from .models import SexToys
from account.mixin import PreviewMixin
from review.forms import ReviewForms
from review.models import ReviewModel


def detail(request, slugname):
    mod = get_object_or_404(SexToys.object.return_published_product(), slug=slugname)

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

    return render(request, 'Products/detail_page.html', context={'object': mod, 'form': form})


class DetailPreview(PreviewMixin, DetailView):
    template_name = 'Products/detail_page.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(SexToys, pk=pk)
