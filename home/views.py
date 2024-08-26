from django.shortcuts import render
from django.views import View
from django.http.request import HttpRequest



class IndexView(View):
    template = 'index.html'

    def get(self, request: HttpRequest):
        blogs =  []
        return render(request , self.template , context={'blogs':blogs})
