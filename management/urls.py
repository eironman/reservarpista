from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ManagementPanel.as_view(), name='management_panel'),
    url(r'^add-sports-center/', views.AddSportsCenter.as_view(), name='add_sports_center'),
    url(r'^edit-sports-center/(?P<center_id>[0-9]+)/$', views.EditSportsCenter.as_view(), name='edit_sports_center'),
    url(r'^delete-sports-center/(?P<center_id>[0-9]+)/$', views.DeleteSportsCenter.as_view(), name='delete_sports_center'),
    url(r'^add-court/(?P<center_id>[0-9]+)/$', views.AddCourt.as_view(), name='add_court'),
    url(r'^edit-court/(?P<court_id>[0-9]+)/$', views.EditCourt.as_view(), name='edit_court'),
    url(r'^delete-court/(?P<court_id>[0-9]+)/$', views.DeleteCourt.as_view(), name='delete_court'),
]
