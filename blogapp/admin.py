from django.contrib import admin
from .models import Blog,Comment, UserProfile, Registration

# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Registration)
