from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login_action, name='login'),
    url(r'^logout/', views.logout_action, name='logout'),
]