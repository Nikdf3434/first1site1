from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import os

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
