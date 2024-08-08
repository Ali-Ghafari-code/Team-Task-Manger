from django.http import Http404
from django.urls import reverse
from django.contrib.auth import login, logout
from .models import User
from django.shortcuts import render, redirect
from django.views import View
from django.utils.crypto import get_random_string
from account.forms import RegisterForm, LoginForm


# from utils.email_service import send_email


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {'register_form': register_form}
        return render(request, 'account/Signup.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            if User.objects.filter(email__iexact=user_email).exists():
                register_form.add_error('email', 'ایمیل وارد شده تکراری میباشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=username
                )
                new_user.set_password(user_password)
                new_user.save()
                # send_email('فعال سازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/active_account.html')
                return redirect(reverse('login_page'))
        context = {'register_form': register_form}
        return render(request, 'account/Signup.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'account/Login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است.')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email', 'نام کاربری و یا کلمه ی عبور اشتباه است')
            else:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده پیدا نشد.')
        context = {'login_form': login_form}
        return render(request, 'account/Login.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None and not user.is_active:
            user.is_active = True
            user.email_active_code = get_random_string(72)
            user.save()
            return redirect(reverse('login_page'))
        raise Http404


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))
