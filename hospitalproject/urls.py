"""
URL configuration for hospitalproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/',views.Registration.as_view(),name='register'),
    path('login/',views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('userslist/',views.UserListView.as_view(),name='userslist'),
    path('doctorlist/',views.UserDoctorView.as_view(),name = 'doctorlist'),
    path('userprofile/',views.UserProfileView.as_view(),name = 'profile'),
    path('adminuserlist/',views.AdminViewUsers.as_view(),name='adminuserlist'),
    path('adminuserlist/<int:pk>/',views.AdminViewUsers.as_view(),name='adminuserlist')

]
