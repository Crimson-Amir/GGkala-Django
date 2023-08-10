from django.shortcuts import redirect, render, HttpResponse
from .models import ReviewModel
from django.views.generic import DetailView
from Products.models import SexToys
from django.contrib import messages
from .forms import ReviewForms


class DeleteReview(DetailView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        review = ReviewModel.objects.get(pk=pk)
        product_id = review.product_slug
        review.delete()
        messages.success(request, "دیدگاه شما با موفقیت حذف شد.")
        return redirect('Products:detail', product_id)

# edit view
# class UpdadeReview(DetailView):
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         title = request.GET.get('review_title')
#         body = request.GET.get('review_content')
#         rating = request.GET.get('rate')
#         ReviewModel(pk=pk).update(comment_title=title, comment_body=body, rate=rating).save()
#         messages.success(request, "دیدگاه شما با موفقیت ویرایش شد.")
#         return redirect('Products:detail', product.slug)
