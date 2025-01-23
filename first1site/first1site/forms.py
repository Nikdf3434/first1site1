from django import forms
from .models import Books, UserFile
# from .models import Login
# from .models import Registration

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title','author_id', 'publishing', 'pages', 'prace']

class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file']

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = Login
#         fields = ['username', 'password']

# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Registration
#         fields = ['username', 'password', 'confirm_password']

