"""
URL configuration for sc22qhtproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app.views import login_view, logout_view, delete_story, story

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/login', login_view, name='login'),                            # for login
    path('api/logout', logout_view, name='logout'),                         # for logout
    path('api/stories', story, name='story'),                               # for posting and getting story
    path('api/stories/<int:story_key>', delete_story, name='delete_story'), # for deleting story
]

