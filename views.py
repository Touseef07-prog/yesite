from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import (LoginRequiredMixin,
UserPassesTestMixin)
from django.views.generic import (ListView,
DetailView,
CreateView,
UpdateView,
DeleteView)
from .models import post

def index(request):
    context ={
    'posts':post.objects.all()
    }

    return render(request, 'index.html',context)

class PostListView(ListView):
    model = post
    template_name = 'index.html'
    context_object_name ='posts'
    ordering =['-date']
    paginate_by = 5

class PostDetailView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = post
    fields =['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = post
    fields =['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = post
    success_url ='/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request, 'about.html')
