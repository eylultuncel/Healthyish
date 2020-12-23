from django.contrib import admin
from foods.views import HomeView, ProfileView, FoodsView, BMIView, DailyCalorieView, DeleteFoodView
from accounts.views import CalculateBMI, PasswordResetView
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('recipes/', include('foods.urls')),
    path('exercises/', include('exercise.urls')),
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('foods/', FoodsView.as_view(), name='foods'),
    path('calculatebmi/', CalculateBMI.as_view(), name="calculatebmi"),
    path('bmi/', BMIView.as_view(), name="bmi"),
    path('dailycalorie/', DailyCalorieView.as_view(), name="dailycalorie"),
    path('delete/<int:food_id>/', DeleteFoodView.as_view(), name="delete"),
    path("select2/", include("django_select2.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
