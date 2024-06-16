from django.urls import path
from .url_views import admin_urls, anonymous_urls, common_urls


app_name = 'gmbe'

urlpatterns = [
    path('families_list', admin_urls.families_list, name='families_list'),
    path('users_list', admin_urls.users_list, name='users_list'),
    path('positions_list', admin_urls.positions_list, name='positions_list'),
    path('paid_guards_list', admin_urls.paid_guards_list, name='paid_guards_list'),
    path('shifts_list', admin_urls.shifts_list, name='shifts_list'),
    path('guarding_list', common_urls.guarding_list, name='guarding_list'),
    path('create_guard_list', admin_urls.create_guard_list, name='create_guard_list'),
    path('save_guard_list', admin_urls.save_guarding_list, name='save_guarding_list'),
    path('get_glist_by_date/<str:date>', common_urls.get_glist_by_date, name='get_glist_by_date'),
    path('get_last_id', anonymous_urls.get_last_id, name='get_last_id'),
    path('get_lists_by_dates/<str:date1>/<str:date2>', common_urls.get_lists_by_dates, name='get_lists_by_dates'),
    path('get_list_by_date_position/<str:date>/<int:position_id>', common_urls.get_list_by_date_position, name='get_list_by_date_position'),
    path('get_glist_by_id/<int:glist_id>', common_urls.get_glist_by_id, name='get_glist_by_id'),
    path('future_gurading_lists', common_urls.future_gurading_lists, name='future_gurading_lists'),
    path('exchange_guard', admin_urls.exchange_guard, name='exchange_guard'),
    path('paid_exchange_guard', admin_urls.paid_exchange_guard, name='paid_exchange_guard'),
    path('cross_exchange_guards', admin_urls.cross_exchange_guards, name='cross_exchange_guards'),

]