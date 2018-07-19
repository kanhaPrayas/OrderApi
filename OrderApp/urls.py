from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/order(?:/(?P<id>[0-9]+))?/$', views.Order.as_view()),
]
