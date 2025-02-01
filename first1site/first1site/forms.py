from django import forms
from .models import Books, UserFile

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title','author_id', 'publishing', 'pages', 'prace']

class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file']