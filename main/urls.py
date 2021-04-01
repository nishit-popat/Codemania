from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('postregister/',views.postregister, name='postregister'),
    path('admin/',views.admin, name='admin'),
    path('plg/', views.plg, name='plg'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('contest_list/', views.contest_list, name='contest_list'),
    path('user_home', views.user_home, name='user_home'),
    path('contest_list/<int:contest_id>/detail',views.detail, name='detail'),
    path('contest_list/<int:contest_id>/<int:problem_id>/problem_playground', views.problem_playground, name='problem_playground'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('lg/',views.login,name='lg'),
]
