from django.db import models

# Create your models here.
class Upload(models.Model):
    file = models.FileField(upload_to='documents/')

def __str__(self):
    return self.file.name