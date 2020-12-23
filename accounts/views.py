from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.contrib import auth
from healthyish.settings import EMAIL_HOST_USER
from .models import User
from .forms import UserAppearanceForm


class SignUpView(View):
    def post(self, request):
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'],
                                                email=request.POST['email'])
                auth.login(request, user)
                return redirect('userappearances')
        else:
            return render(request, 'signup.html', {'error': 'Passwords didnt match'})

    def get(self, request):
        return render(request, 'signup.html')


class LoginView(View):
    def post(self, request):
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Username or password is incorrect.'})

    def get(self, request):
        return render(request, 'login.html')


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        auth.logout(request)
        return redirect('home')


class CalculateBMI(View):
    def post(self, request):
        form = UserAppearanceForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            bmi = int((weight * 10000) / (height * height))
            if sex.name == "Male":
                dailycalorie = int((66 + (13.7 * weight) + (5 * height) - (6.8 * age)) * 1.2)
            elif sex.name == "Female":
                dailycalorie = int((665 + (9.6 * weight) + (1.8 * height) - (4.7 * age)) * 1.2)
            return render(request, 'calculateBMI.html', {'form': form, 'bmi': bmi, 'dailycalorie': dailycalorie})
        else:
            error = "Your form is not valid, please try again."
            return render(request, 'calculateBMI.html', {'form': form, 'error': error})

    def get(self, request):
        form = UserAppearanceForm
        return render(request, 'calculateBMI.html', {'form': form})


class PasswordResetView(View):
    def post(self, request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'healthyish',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email,  EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
            else:
                password_reset_form = PasswordResetForm()
                return render(request, 'password_reset.html', {"password_reset_form": password_reset_form,
                                                               'error': 'User does not exist.'})
        else:
            password_reset_form = PasswordResetForm()
            return render(request, 'password_reset.html', {"password_reset_form": password_reset_form,
                                                           'error': 'User does not exist.'})

    def get(self, request):
        password_reset_form = PasswordResetForm()
        return render(request, "password_reset.html", {"password_reset_form": password_reset_form})


class UserAppearancesView(LoginRequiredMixin, View):
    def post(self, request):
        form = UserAppearanceForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.bmi = (user.weight * 10000) / (user.height * user.height)
            sex = form.cleaned_data['sex']
            age = form.cleaned_data['age']
            if sex.name == "Male":
                user.dailycalorie = (66 + (13.7 * user.weight) + (5 * user.height) - (6.8 * age)) * 1.37
            elif sex.name == "Female":
                user.dailycalorie = (665 + (9.6 * user.weight) + (1.8 * user.height) - (4.7 * age)) * 1.37
            user.save()
            return redirect('home')
        else:
            error = "Your form is not valid, please try again."
            return render(request, 'userappearance.html', {'form': form, 'error': error})

    def get(self, request):
        form = UserAppearanceForm
        return render(request, 'userappearance.html', {'form': form})


class ProfileSettingsView(LoginRequiredMixin, View):
    def post(self,request):
        user = request.user

        if len(request.POST.get('username')) != 0:
            try:
                user = User.objects.get(username=request.POST.get('username'))
                return render(request, 'profile_settings.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user.username = request.POST.get('username')

        if len(request.POST.get('email')) != 0:
            user.email = request.POST.get('email')

        if len(request.POST.get('password1')) != 0 & len(request.POST.get('password2')) != 0:
            if request.POST.get('password1') == request.POST.get('password2'):
                user.set_password(request.POST.get('password1'))
        user.save()
        return redirect('home')

    def get(self, request):
        user = request.user
        return render(request, 'profile_settings.html', {'user': user})
