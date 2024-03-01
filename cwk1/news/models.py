from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Story(models.Model):
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=32, choices=[('pol', 'Politics'), ('art', 'Art'), ('tech', 'Technology'), ('trivia', 'Trivia')])
    region = models.CharField(max_length=32, choices=[('uk', 'UK'), ('eu', 'European'), ('w', 'World')])
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    details = models.CharField(max_length=128)

    def __str__(self):
        return self.title
