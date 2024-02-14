from django.urls import path
from .url_views import admin_urls


app_name = 'gmbe'

urlpatterns = [
    path('families_list', admin_urls.families_list, name='families_list'),
    path('users_list', admin_urls.users_list, name='users_list')
]