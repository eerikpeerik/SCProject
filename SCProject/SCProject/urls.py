from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Redirect the root URL to the login page
    path('', lambda request: redirect('login')),
    
    # Include your app's URLs for the list functionality
    path('list/', include('list.urls')),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Registration URL if you have one (adjust the view import accordingly)
    # path('register/', list_views.register, name='register'),

    path('admin/', admin.site.urls),
]
