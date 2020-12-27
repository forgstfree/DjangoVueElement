from django.db import models

# Create your models here.

class LogFileModel(models.Model):
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='logfile/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
