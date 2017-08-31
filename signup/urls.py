from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^owner/$', views.signup_page_owner, name='signup_page_owner'),
]
