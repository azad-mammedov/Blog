from django.shortcuts import render

from django.views import View


class LoginView(View):
    template = 'login.html'
    
    def get(self, request):
        return render(request , self.template)
    

class RegisterView(View):
    template = 'register.html'

    def get(self, request):
        return render(request, self.template)

class ChangePasswordView(View):
    template = 'change_password.html'

    def get(self, request):
        return render(request, self.template)