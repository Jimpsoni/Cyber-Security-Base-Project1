"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from src.views import login_view, upload, logout_view, search, usersettings, deleteuser, create_user
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.urls')),

    # Login/logout
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Upload
    path('upload/', upload, name='upload'),

    # Search
    path('search/', search, name='search'),

    # Settings
    path('settings/', usersettings, name='settings'),

    # Delete and create user
    path('deleteuser/', deleteuser, name='deleteuser'),
    path('createuser/', create_user, name='createuser'),

]

# To serve static files
urlpatterns += staticfiles_urlpatterns()