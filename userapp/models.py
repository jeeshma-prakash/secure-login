from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name