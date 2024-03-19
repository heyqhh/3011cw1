from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# author table
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# story table
class Story(models.Model):
    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    ]

    REGION_CHOICES = [
        ('uk', 'United Kingdom'),
        ('eu', 'European Union'),
        ('w', 'World'),
    ]

    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=10, choices=REGION_CHOICES)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline