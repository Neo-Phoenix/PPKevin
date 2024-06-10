from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('register', views.register, name="register"),
    path('signin', views.signin, name="signin"),
    path('login', views.login, name="login"),
    path('overview', views.overview, name="overview"),
    path('logout_view', views.logout_view, name="logout"),
    path('event-manager', views.event_manager, name="event-manager")
]