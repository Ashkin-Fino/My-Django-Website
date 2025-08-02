from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm

class ViewProfile(View):

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            user = request.user
            return render(request, "UserProfile/view_profile.html", {"user": user})
        return render(request, "UserProfile/login_or_signup.html")
    

class EditProfile(View):

    def get(self, request: HttpRequest):
        return HttpResponse("We are currently under development. Please come back later :)")

    def post(self, request: HttpRequest):
        pass


class Signup(View):

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
        return render(request, "UserProfile/signup.html", {"form": CustomUserCreationForm()})

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login', permanent=True)


class Login(View):

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return render(request, "UserProfile/login_successful.html", {"user": request.user, "first_attempt": False})
        else:
            return render(request, "UserProfile/login.html", {"message": "Enter your credentials to login to your account"})

    def post(self, request: HttpRequest):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user_obj = User.objects.filter(username=username).first()
        user = authenticate(request, username=username, password=password)
        if not user_obj:
            return render(request, "UserProfile/login.html", {"message": "Invalid username. Please try again"})
        elif not user:
            return render(request, "UserProfile/login.html", {"message": "Invalid password. Please try again"})
        else:
            login(request, user)
            return render(request, "UserProfile/login_successful.html", {"user": user_obj, "first_attempt": True})


class Logout(View):

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
            return render(request, "UserProfile/logout_successful.html")
        else:
            return render(request, "UserProfile/login_or_signup.html")
