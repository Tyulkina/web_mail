from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete = models.PROTECT)
    likes = models.ManyToManyField(User,related_name='question_likes_user')
    objects = QuestionManager()
    
    def __str__(self):
        return self.title
    
class Answer(models.Model):    
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add = True)
    question = models.ForeignKey(Question, on_delete = models.PROTECT)
    author = models.ForeignKey(User, on_delete = models.PROTECT)


class Session(models.Model):
    key = models.CharField(unique=True, max_length=30)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    expires = models.DateTimeField()
