"""justdoit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from doit import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),

    # Doits
    path('currentdoits/', views.currentdoits, name='currentdoits'),
    path('completed/', views.completed, name='completed'),
    path('doit/<int:doit_pk>', views.viewdoit, name='viewdoit'),
    path('doit/<int:doit_pk>/complete', views.completedoit, name='completedoit'),
    path('doit/<int:doit_pk>/delete', views.deletedoit, name='deletedoit'),
    path('create/', views.createdoits, name='createdoits'),
    path('', views.home, name='home'),


]
