from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),  # removed trailing slash
    path('signin', views.signin, name='signin'),  # removed trailing slash
]