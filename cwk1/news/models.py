from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Story(models.Model):
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=32, choices=[('pol', 'Politics'), ('art', 'Art'), ('tech', 'Technology'), ('trivia', 'Trivia')])
    region = models.CharField(max_length=32, choices=[('uk', 'UK'), ('eu', 'European'), ('w', 'World')])
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline
