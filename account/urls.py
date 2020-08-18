from django.urls import path,include
from . import views
urlpatterns = [ 
    path('', views.home,name="home"),
    path('home/', views.home,name="home"),
    path('homesc/', views.homerequest,name="homerequest"),
    path('login/', views.loginuser,name="loginuser"),
    path('register/', views.register,name="register"),
    path('logout/', views.logoutuser,name="logoutuser"),

    


]
