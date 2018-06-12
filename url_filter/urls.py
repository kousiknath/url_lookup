from django.conf.urls import url

from url_filter.views import URLFilter

urlpatterns = [
    url('add', URLFilter.as_view(), name='add_url'),
    url('', URLFilter.as_view(), name='filter_url')
]