from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
]