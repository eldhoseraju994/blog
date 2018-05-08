from django.conf.urls import url
from django.conf import settings
from django.urls import path
from .views import NewBlogView, blogs, Add_User,BlogDetailView,AddCommentToBlogView,LoginView,LogoutView,AddReplyToComment


urlpatterns = [
	path('', blogs, name='blogs'),
	path('user/new/', Add_User, name='Add_User'),
	path('user/login/', LoginView.as_view(), name='log_in'),
	path('user/logout/', LogoutView.as_view(), name='log_out'),
	path('blog/<int:pk>/',BlogDetailView.as_view(), name='blog_detail'),
	path('blog/blog_new/',NewBlogView.as_view() , name='blog_new'),
	path('blog/<int:pk>/comment/',AddCommentToBlogView.as_view(), name='add_comment_to_blog'),
	path('blog/<int:pk>/reply/',AddReplyToComment.as_view(), name='add_reply'),
    #url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),"""
    ]
