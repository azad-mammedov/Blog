from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseForbidden

from post.models import Post
from post.forms import PostForm

class PostCreateView(LoginRequiredMixin,View):
    template = 'post_create.html'


    def get(self, request):
        form = PostForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = request.user
            new_post.save()
            messages.success(request, 'Post created successfully')
            return redirect('index')  
        return render(request, self.template, {'form': form})

class PostUpdateView(LoginRequiredMixin,View):
    template = 'post_detail.html'


    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        is_author = request.user == post.created_by
        form = PostForm(instance=post)
        return render(request, self.template, {'form': form , 'is_author':is_author , 'post':post})
    

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        is_author = request.user == post.created_by
        if not is_author:
            return HttpResponseForbidden('You are not allowed')

        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, self.template, {'form': form , 'is_author':is_author , 'post':post})

class PostDeleteView(LoginRequiredMixin,View):
    template = 'post_confirm_delete.html'


    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, self.template, {'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user != post.created_by:
            return HttpResponseForbidden('You are not allowed')
        messages.success(request,'Post deleted Successfully')
        post.delete()
        return redirect('index')
