from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Client
from appointement.models import Appointment, Reschedule, Notification
# Create your views here.


def home(request):
    return render(request, 'app/index.html', {})


def register_user(request):
    if request.method == "POST":
        data = request.POST
        if User.objects.filter(username=data['name']):
            messages.warning(request, 'Account already exist.')
            return redirect('register')
        user = User(username=data['name'], email=data['email'])
        user.set_password(data['password'])
        user.save()
        client = Client(user=user, phone=data['phone'], address=data['address'])
        client.save()
        messages.success(request, 'Account registered successfully.')
        return redirect('login')
    return render(request, 'app/reg.html', {})


def login_user(request):
    if request.method == "POST":
        data = request.POST
        user = authenticate(username=data['name'], password=data['password'])
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('profile')
            return redirect('home')

        else:
            messages.warning(request, 'Invalid Username or Password')
            return redirect('login')
    return render(request, 'app/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('login')


def profile(request):
    context = {}
    if request.user.is_superuser:
        html_page = 'app/profile.html'
        reschedules = Reschedule.objects.filter(waited=True).order_by('-id')
        context['reschedules'] = reschedules
    else:
        html_page = 'app/client_profile.html'
        appointments = Appointment.objects.filter(client__user=request.user)
        notifications = Notification.objects.filter(client__user=request.user)
        context['appointments'] = appointments
        context['notifications'] = notifications

    return render(request, html_page, context)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'app/password_reset.html'
    email_template_name = 'app/password_reset_email.html'
    subject_template_name = 'app/reset_password_subj.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')

