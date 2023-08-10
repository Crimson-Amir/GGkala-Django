from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from Products.models import SexToys
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixin import (FieldMixin, SuperUserAndStaffMixin, FormValidMixin,
                    AccsesMixin, JustSuperUserMixin, AccsesToAdminPanel,
                    JustSuperUser)

from .forms import ProfileForms
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from GGKala.tokens import account_activation_token
from django.core.mail import EmailMessage


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return reverse_lazy('account:dashboard')
        else:
            return reverse_lazy('Home:home')


class Home(AccsesToAdminPanel, ListView):
    template_name = "registration/dashboard.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SexToys.object.all()[:6]
        elif self.request.user.is_staff:
            return SexToys.object.filter(publisher=self.request.user)[:6]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['new_user'] = User.objects.all()[:5]
        return context


class ProductAdmin(SuperUserAndStaffMixin, ListView):
    template_name = "registration/products_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SexToys.object.all()
        elif self.request.user.is_staff:
            return SexToys.object.filter(publisher=self.request.user)


class CreatProduct(SuperUserAndStaffMixin, FieldMixin, FormValidMixin, CreateView):
    model = SexToys
    template_name = "registration/creat_or_update_product.html"


class UpdateProduct(AccsesMixin, FieldMixin, FormValidMixin, UpdateView):
    model = SexToys
    template_name = "registration/creat_or_update_product.html"


class DeleteProduct(JustSuperUserMixin, DeleteView):
    model = SexToys
    success_url = reverse_lazy("account:products")
    template_name = 'registration/delete_product.html'


class Profile(SuperUserAndStaffMixin, UpdateView):
    form_class = ProfileForms
    model = User
    template_name = "registration/profile.html"
    success_url = reverse_lazy('account:dashboard')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs


class Users(JustSuperUser, ListView):
    model = User
    template_name = "registration/users-show.html"

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['just_super'] = User.objects.filter(is_staff=True)
        return context

# class Signup(CreateView):
#     form_class = SignupForm
#     template_name = 'registration/signup.html'

# def form_invalid(self, form):
#     we_user = User.objects.get(username=form.data['username'])
#     if we_user.is_active is False:
#         we_user.delete()
#         # return reverse_lazy('signup')
#     else:
#         return reverse_lazy('signup')

# def form_valid(self, form):
#     user = form.save(commit=False)
#     user.is_active = False
#     user.save()
#     current_site = get_current_site(self.request)  # get site domin
#     mail_subject = 'فعال سازی حساب شما در جی‌جی کالا'
#     message = render_to_string('registration/acc_active_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#     })
#     to_email = form.cleaned_data.get('email')
#     email = EmailMessage(
#         mail_subject, message, to=[to_email]
#     )
#     email.send()
#     return HttpResponse('Please confirm your email address to complete the registration')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        try:
            we_user = User.objects.get(username=form.data['username'])
            if we_user.is_active is False:
                we_user.delete()
        except User.DoesNotExist:
            pass

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('ممنون برای نهایی کردن ثبت نام.')
    else:
        return HttpResponse('لینک باطل شده است')
