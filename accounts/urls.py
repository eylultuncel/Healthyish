from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/',views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('userappearances/', views.UserAppearancesView.as_view(), name='userappearances'),
    path('settings/', views.ProfileSettingsView.as_view(), name='settings'),

]