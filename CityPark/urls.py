from django.contrib import admin
from django.urls import path, include
from catalog.views import *
from django.contrib.auth.views import LogoutView
from users.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', login_view, name='login'),
    path('registration/', register_view, name='registration'),
    path('basket/', basket, name='basket'),
    path('favourites/', favourites, name='favourites'),
    path("checkout/", checkout, name="checkout"),
    path("order-success/<int:order_id>/", order_success, name="order_success"),
    path('profile/', profile, name='profile'),
    path('', include('restaurant.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
