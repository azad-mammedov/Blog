from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import RegistrationForm, LoginForm, CustomPasswordChangeForm


class RegisterView(View):
    template = 'register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')
        return render(request, self.template, {'form': form})

class LoginView(View):
    template = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful.')
                next_ = request.GET.get('next')
                if next_:
                    return redirect(next_)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid credentials')
        return render(request, self.template, {'form': form})


class LogoutView(View):


    def get(self, request):
        auth_logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('index')



class ChangePasswordView(LoginRequiredMixin,View):
    template = 'change_password.html'
    login_url = reverse_lazy('login')

    def get(self, request):
        form = CustomPasswordChangeForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('index')
            else:
                form.add_error('old_password', 'Current password is incorrect')
        return render(request, self.template, {'form': form})
