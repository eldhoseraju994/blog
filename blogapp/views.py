from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Blog
from .forms import MyRegistrationForm,NewBlog
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView 

def blogs(request):
    blog = Blog.objects.all()
    return render(request, 'blogapp/home.html', {'blog':blog})
    #return render(request, 'blogapp/home.html', {})

def Add_User(request):
    if request.method == "POST":
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blogs', pk=post.pk)
    else:
        form = MyRegistrationForm()
    return render(request, 'blogapp/UserRegistration.html', {'form': form})

# def blog_new(request):
#     if request.method == "POST":
#         form = NewBlogs(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('blogs', pk=post.pk)
#     else:
#         form = NewBlogs()
#     return render(request, 'blogapp/BlogNew.html', {'form': form})


class NewBlogView(CreateView):
    model = Blog
    form_class = NewBlog
    template_name = 'blogapp/BlogNew.html'

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/detail_view.html'


    


