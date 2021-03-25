from . import views
from django.urls import path


urlpatterns = [
    path('',views.login, name='login'),
    path('admin',views.admin, name='admin'),
    path('register',views.register, name='register'),
    path('plg/', views.plg, name='plg'),
    path('login',views.home, name='home'),
    path('contest_list/', views.contest_list, name='contest_list'),
    path('contest_list/<int:contest_id>/detail',views.detail, name='detail'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('lg',views.login,name='lg')
]
