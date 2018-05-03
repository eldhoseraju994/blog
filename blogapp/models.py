from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

"""class UserProfile(AbstractUser):

     user_mobile = models.IntegerField(max_length=10, null=True)
     user_bank_name=models.CharField(max_length=100,null=True)
     user_bank_account_number=models.CharField(max_length=50, null=True)
     user_bank_ifsc_code = models.CharField(max_length=30,null=True)
     user_byt_balance = models.IntegerField(max_length=20, null=True)"""

class Blog(models.Model):
	title = models.CharField(max_length=200)
	img = models.ImageField(upload_to='blogapp/images')
	published_date = models.DateTimeField(blank=True, null=True,default=timezone.now())
	author = models.CharField(max_length=100)
	caption = models.CharField(max_length=200)
	text = models.TextField()

	def publish(self):
	    self.published_date = timezone.now()
	    self.save()
	def __str__(self):
		return self.title

class UserProfile(AbstractUser):
	"""docstring for Register"""
	first_name = models.CharField(max_length=50,blank=True, null=True)
	last_name = models.CharField(max_length=50,blank=True, null=True)
	#user = models.CharField(max_length=50,blank=True, null=True)
	#password = models.CharField(max_length=50,blank=True, null=True)
	status = models.CharField(max_length=1, blank=True, null=True )
	
	def publish(self):
		self.save()

	def __str__(self):
		return self.first_name,self.last_name

class Comments(models.Model):
	"""docstring for Register"""
	blogid = models.CharField(max_length=50,blank=True, null=True)
	userid = models.CharField(max_length=50,blank=True, null=True)
	comments =models.CharField(max_length=50,blank=True, null=True)
	rply = models.CharField(max_length=50,blank=True, null=True)
	
	def publish(self):
		self.save()

	def __str__(self):
		return self.first_name,self.last_name