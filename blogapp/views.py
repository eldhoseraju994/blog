import  json
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View

from .models import Blog, Comment, UserProfile
from .forms import MyRegistrationForm, NewBlogForm, CommentForm, LoginForm, ReplyForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import logout


def blogs(request):
    context = {}
    context['blog'] = Blog.objects.all()
    context['comment'] = Comment.objects.all()
    return render(request, 'blogapp/home_user.html', context)
    #return render(request, 'blogapp/home.html', {})

def Add_User(request):
    if request.method == "POST":
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return render(request, 'blogapp/login.html', {'form':LoginForm()})

    else:
        form = MyRegistrationForm()
    return render(request, 'blogapp/UserRegistration.html', {'form': form})


class LoginView(FormView):
    
    form_class = LoginForm
    template_name = 'blogapp/login.html'
    success_url = '.'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect('/')

        return super(LoginView, self).form_valid(form)


class LogoutView(FormView):

    def get(self, request, *args, **kwargs):
        #print (self.request.user.username)
        logout(request)
        return HttpResponseRedirect('/')

class  AddCommentToBlogView(LoginRequiredMixin, View):
    model = Comment
    # #form_class = CommentForm
    # # context['reply'] = Reply.objects.all()
    template_name ='blogapp/blog_detail.html'
    #
    # def form_valid(self, form):
    #     #print (self.kwargs)
    #     self.object = form.save(commit=False)
    #     blog = Blog.objects.get(pk=self.kwargs.get('pk'))
    #     userna= self.request.user.username
    #     self.object.blog = blog
    #     self.object.username=userna
    #     self.object.save()
    #     url = reverse('blog_detail', kwargs={'pk': int(self.kwargs.get('pk')) })
    #     return HttpResponseRedirect(url)

    def post(self, request, *args, **kwargs):
        blog_id = request.POST.get('blog_id')
        blog_obj=Blog.objects.get(id=blog_id)
        comment = request.POST.get('comment')
        obj = Comment.objects.create(blog=blog_obj,text=comment,username=self.request.user)
        return HttpResponse(json.dumps({'comment': obj.text,'date':str(obj.created_date),'username':obj.username.username}), content_type="application/json")
class  AddReplyToComment(CreateView):
    model = Comment
    form_class = CommentForm
    # context['reply'] = Reply.objects.all()
    template_name ='blogapp/add_reply.html'

    def get_context_data(self, **kwargs):
       context = super(AddReplyToComment, self).get_context_data(**kwargs)
       comment = Comment.objects.get(pk=self.kwargs.get('pk'))
       context['comment'] = comment
       return context
    def form_valid(self, form):
        #print (self.kwargs)
        self.object = form.save(commit=False)
        comment = Comment.objects.get(pk=self.kwargs.get('pk'))
        userna= self.request.user.username
        self.object.parent_comment = comment
        self.object.username=userna
        self.object.save()
        url = reverse('add_reply', kwargs={'pk': int(self.kwargs.get('pk')) })
        return HttpResponseRedirect(url)


class NewBlogView(CreateView):
    model = Blog
    form_class = NewBlogForm
    template_name = 'blogapp/BlogNew.html'

class BlogDetailView(LoginRequiredMixin,DetailView):
    model = Blog
    template_name = 'blogapp/detail_view_blog.html'

    def form_valid(self, form):
        return HttpResponseRedirect('blogapp/detail_view_blog.html')




"""def add_comment_to_blog(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detail_view_blog', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blogapp/add_comment_to_post.html', {'form': form})
"""

    


