from django.conf.urls import url
from django.conf import settings
from .views import NewBlogView, blogs, Add_User,BlogDetailView
urlpatterns = [
	url(r'^$', blogs, name='blogs'),
	url(r'^user/new/$', Add_User, name='Add_User'),
  	url(r'^post/(?P<pk>\d+)/$',BlogDetailView.as_view(), name='blog_detail'),
    url(r'^blog/blog_new/$',NewBlogView.as_view() , name='blog_new'),

    #url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),"""
    ]
