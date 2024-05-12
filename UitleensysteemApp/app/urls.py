from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('login', views.login, name="login"),
    path('overview', views.overview, name="overview"),

]