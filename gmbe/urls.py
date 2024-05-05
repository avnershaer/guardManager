from django.urls import path
from .url_views import admin_urls


app_name = 'gmbe'

urlpatterns = [
    path('families_list', admin_urls.families_list, name='families_list'),
    path('users_list', admin_urls.users_list, name='users_list'),
    path('positions_list', admin_urls.positions_list, name='positions_list'),
    path('shifts_list', admin_urls.shifts_list, name='shifts_list'),
    path('guarding_list', admin_urls.guarding_list, name='guarding_list'),
    path('create_guard_list', admin_urls.create_guard_list, name='create_guard_list'),
    path('save_guard_list', admin_urls.save_guarding_list, name='save_guarding_list'),
    path('get_glist_by_date/<str:date>', admin_urls.get_glist_by_date, name='get_glist_by_date'),
]