from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from account.models import User


def home_page(request):
    return render(request, 'Home/home.html')


class PublisherList(ListView):
    paginate_by = 28
    template_name = 'Home/publisher_list.html'

    def get_queryset(self):
        global publisher
        username = self.kwargs.get('publisher')
        publisher = get_object_or_404(User, username=username)
        return publisher.publisher_Products.return_published_product()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = publisher
        return context
