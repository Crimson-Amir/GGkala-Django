from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from account.views import Login, signup, activate


urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path('signup/', signup, name="signup"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('Home.urls')),
    path('account/', include('account.urls')),
    path('category/', include('Category.urls')),
    path('products/', include('Products.urls')),
    path('review/', include('review.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
