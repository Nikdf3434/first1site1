from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import os

class Authors(models.Model):
    surname_and_initials = models.CharField(max_length=100, blank=False)
    years_of_life = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.surname_and_initials
        
class Books(models.Model):
    title = models.CharField(max_length=100, blank=False)
    author_id = models.ForeignKey(Authors, on_delete=models.CASCADE, default=1)
    publishing = models.CharField(max_length=100, blank=False, default='-')
    pages = models.IntegerField()
    prace = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.title}: {self.author_id}: {self.publishing}'

class NewUser(AbstractUser):
    pass

def v(file):
    ext = os.path.splitext(file.name)[-1].lower()
    print(ext)
    if ext != '.csv':
        raise ValidationError('Разрешены только файлы формата CSV.')

class UserFile(models.Model):
    user = models.ForeignKey('NewUser', on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="users_file/",
        blank=True,
        null=True,
        validators=[v]
    )
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.file}: {self.data}'