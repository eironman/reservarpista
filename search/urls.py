from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_sports_center/(?P<id>[0-9]+)/$', views.get_sports_center, name='get_sports_center'),
    url(r'^go_to_page/(?P<page>[0-9]+)/$', views.go_to_page, name='go_to_page'),
    url(r'^send_booking_request/$', views.send_booking_request, name='send_booking_request'),
    url(r'^$', views.index, name='search_results'), # /sport_slug/city_slug/
]
