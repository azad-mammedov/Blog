from django.shortcuts import render
from django.views import View
from django.http.request import HttpRequest
from django.core.paginator import Paginator

from post.models import Post



class IndexView(View):
    template = 'index.html'

    def get(self, request: HttpRequest):
        posts = Post.objects.all().order_by('-pk')
        paginator = Paginator(posts , 3)
        page = request.GET.get('page','1')
        page_obj  = paginator.get_page(page)
        return render(request , self.template , context={'blogs':posts , 'page_obj':page_obj})


