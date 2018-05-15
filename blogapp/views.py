import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View


from .models import Blog, Comment, UserProfile ,Registration
from .forms import MyRegistrationForm, NewBlogForm, CommentForm, LoginForm, ReplyForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout

from django.core.mail import send_mail
from django.core.signing import Signer
from django.template.loader import render_to_string


from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin

from django.contrib.auth.decorators import login_required
from django.shortcuts import render



def blogs(request):
    context = {}
    context['blog'] = Blog.objects.all()
    context['comment'] = Comment.objects.all()
    return render(request, 'blogapp/home_user.html', context)
    # return render(request, 'blogapp/home.html', {})

@login_required
def home(request):
    return render(request, 'user/home_social.html')





def Add_User(request):
    if request.method == "POST":
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_active=False
            post.save()
            signer = Signer()

            signed_value = signer.sign(post.username)
            key = ''.join(signed_value.split(':')[1:])
            reg_obj = Registration.objects.create(user=post, key=key)
            msg_html = render_to_string('blogapp/mail_validation.html', {'key': key})
            #import pdb;pdb.set_trace()
            send_mail("123", "123", 'anjitha.test@gmail.com', [post.username ], html_message=msg_html, fail_silently=False)
            #send_mail('Acount Activated', 'post.author Activated succesfully', 'eldhosetemp@gmail.com', [post.username ], html_message=msg_html, fail_silently=False)
            return render(request, 'blogapp/check_mail.html',)

    else:
        form = MyRegistrationForm()
    return render(request, 'blogapp/UserRegistration.html', {'form': form})


class RegistrationSuccess(TemplateView):
    print("class in")
    template_name = 'blogapp/registration_success.html'

    def get_context_data(self, **kwargs):
        print("method innnnnn")
        context = super(RegistrationSuccess, self).get_context_data(**kwargs)
        key = self.kwargs.get("key")
        try:
            reg_obj = Registration.objects.get(key=key)
            print("reg_obj created innnn")
            reg_obj.user.is_active = True
            reg_obj.save()
            reg_obj.user.save()
            context.update({'user': reg_obj, 'status': True})


        except Registration.DoesNotExist:
            print("excpet case deactivate false innnnnn")
            context.update({'status': False})

        return context


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
        # print (self.request.user.username)
        logout(request)
        return HttpResponseRedirect('/')




# class BlogUpdate(UpdateView):
#     model = Blog


class AddCommentToBlogView(LoginRequiredMixin, View):
    model = Comment
    # #form_class = CommentForm
    # # context['reply'] = Reply.objects.all()
    template_name = 'blogapp/blog_detail.html'

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
        blog_obj = Blog.objects.get(id=blog_id)
        comment = request.POST.get('comment')
        obj = Comment.objects.create(blog=blog_obj, text=comment, username=self.request.user)
        return HttpResponse(
            json.dumps({'comment': obj.text, 'date': str(obj.created_date), 'username': obj.username.username}),
            content_type="application/json")

""""""
class AddReplyToComment(CreateView):
    model = Comment
    form_class = CommentForm
    # context['reply'] = Reply.objects.all()
    template_name = 'blogapp/add_reply.html'

    def get_context_data(self, **kwargs):
        context = super(AddReplyToComment, self).get_context_data(**kwargs)
        comment = Comment.objects.get(pk=self.kwargs.get('pk'))
        context['comment'] = comment
        return context

    def form_valid(self, form):
        # print (self.kwargs)
        # import pdb;pdb.set_trace()
        self.object = form.save(commit=False)
        comment = Comment.objects.get(pk=self.kwargs.get('pk'))
        userna = self.request.user.username
        self.object.parent_comment = comment
        self.object.username = UserProfile.objects.get(username=userna)
        self.object.save()
        url = reverse('add_reply', kwargs={'pk': int(self.kwargs.get('pk'))})
        return HttpResponseRedirect(url)


# add reply to comment using ajax
class AddReplyToCommentView(LoginRequiredMixin, View):
    model = Comment
    template_name = 'blogapp/blog_detail.html'

    def post(self, request, *args, **kwargs):
        parent_comment_id = request.POST.get('parent_id')
        parent_comment = Comment.objects.get(pk=parent_comment_id)
        # blog_obj=Blog.objects.get(id=blog_id)
        reply = request.POST.get('reply')
        obj = Comment.objects.create(text=reply, username=self.request.user, parent_comment=parent_comment)
        return HttpResponse(
            json.dumps({'comment': obj.text, 'date': str(obj.created_date), 'username': obj.username.username}),
            content_type="application/json")


class NewBlogView(SuperuserRequiredMixin,CreateView):
    model = Blog
    form_class = NewBlogForm
    #template_name = u"path/to/template.html"
    template_name = 'blogapp/BlogNew.html'
    success_url = '/'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.super_obj = self.request.user
        self.object.save()
        return HttpResponseRedirect('/')


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blogapp/detail_view_blog.html'

    def form_valid(self, form):
        return HttpResponseRedirect('blogapp/detail_view_blog.html')

class BlogDeleteView(View):
    Model = Blog
    #template_name = 'blogapp/login.html'
    success_url = '.'

    def get(self, request, *args,** kwargs):
        #article = get_object_or_404(id=request.POST['article_id'])
        blog_obj = Blog.objects.get(pk=self.kwargs.get('pk'))
        #print (("deletinggggggggggggggggggggggggggg", blog_obj))
        blog_obj.delete()
        return HttpResponseRedirect('/')

"""class BlogEdit(FormView):
    Model = Blog
    template_name = ''
    def get(self ,request, *args,** kwargs):
        blog_obj = Blog.objects.get(pk=self.kwargs.get(pk))
        return render(request, 'blogapp/blog_edit.html', {'blog':blog_obj})"""

class BlogEdit(UpdateView):
    model = Blog
    template_name = 'blogapp/blog_edit.html'
    fields = ['title', 'author', 'caption', 'text', 'img']
    success_url = '/'


















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
