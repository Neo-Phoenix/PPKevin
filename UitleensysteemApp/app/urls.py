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
     path('event/create/', views.event_create, name='event_create'),
     path('event_manager/', views.event_manager, name='event_manager'),
     path('event/<int:pk>/edit/', views.event_update, name='event_update'),
    path('event/delete/<int:pk>/', views.event_delete, name='event_delete'),
]