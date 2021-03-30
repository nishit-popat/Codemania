from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('register/register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('user_home/', views.user_home, name='user_home'),
    path('logout', views.logout, name='logout'),
    path('admin/',views.admin, name='admin'),
    path('plg/', views.plg, name='plg'),
    path('contest_list/', views.contest_list, name='contest_list'),
    path('contest_list/<int:contest_id>/detail',views.detail, name='detail'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('lg/',views.login,name='lg')
]
