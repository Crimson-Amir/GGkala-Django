from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from Products.models import SexToys


class FieldMixin:

    def dispatch(self, request, *args, **kwargs):
        self.fields = ["reason_for_return", "title", "photo", "price", "color", "category", "brand",
                       "size", "about", "slug", "inventory", "publish", 'off']

        if request.user.is_superuser:
            self.fields.append('publisher')

        return super().dispatch(request, *args, **kwargs)

#
# class LoginedBack:
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('Home:home')
#         else:
#             return super().dispatch(request, *args, **kwargs)


class AccsesToAdminPanel:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            if request.user.is_authenticated:
                return redirect('Home:home')
            else:
                return redirect('login')


class SuperUserAndStaffMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("not found")


class JustSuperUser:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("not found")


class FormValidMixin:
    def form_valid(self, form):
        if self.request.user.is_superuser:
            a = form.save(commit=False)
            a.real = a.price - (a.price * a.off / 100)
            a.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.publisher = self.request.user
            self.obj.real = self.obj.price - (self.obj.price * self.obj.off / 100)
            if not self.obj.publish == "pending":
                self.obj.publish = 'unpublished'
            self.obj.save()

        return super().form_valid(form)


class AccsesMixin:

    def dispatch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(SexToys, pk=pk)
        if product.publisher == request.user and product.publish in ['unpublished', 'returned'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("not found")


class JustSuperUserMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("not found")


class PreviewMixin:

    def dispatch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(SexToys, pk=pk)
        if product.publisher == request.user and product.publish in ['unpublished', 'returned', 'pending'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("not found")
