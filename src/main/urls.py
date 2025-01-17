from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from bulletion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('bulletion.urls')),
    path('accounts/login/',auth_views.LoginView.as_view(),name="login"),
    path('accounts/logout/',views.logout_view,name="logout"),
    path('accounts/signup/',views.signup,name="signup"),
    path('accounts/profile/',views.profile,name="profile"),



]
