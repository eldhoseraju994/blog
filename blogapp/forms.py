       

from django import forms            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import UserCreationForm      
from .models import UserProfile
from .models import Blog, Comment
from django.contrib.auth import get_user_model
from django import forms

class MyRegistrationForm(UserCreationForm):
    
    class Meta:
    	model = UserProfile
    	fields = ('first_name', 'last_name','username')

    """def save(self,commit = False):   
                    user = super(MyRegistrationForm, self).save(commit = False)
                    user.email = self.cleaned_data['email']
                    user.user_mobile = self.cleaned_data['mobile']
                    user.set_password(self.cleaned_data["password1"])
            
                    user_default = User.objects.create_user(self.cleaned_data['username'],
                                                            self.cleaned_data['email'],
                                                            self.cleaned_data['password1'])
                    user_default.save()
            
                    if commit:
                         user.save()
            
                     return user
            		"""

class NewBlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('title', 'author','caption','text','img')

class CommentForm(forms.ModelForm):

    text = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['class'] = 'my_text'

    class Meta:
        model = Comment
        fields = ('text',)

#ReplyForm not used any where
class ReplyForm(forms.ModelForm):

    text=forms.CharField(max_length=50)

    class Meta:
        model = Comment
        fields = ('text',)

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username','password' )

    # def clean(self):
    #     return self.cleaned_data