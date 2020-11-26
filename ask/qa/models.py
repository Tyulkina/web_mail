from django.db import models
from django.contrib.auth.models import User

class QuestionManager(models.Manager):
    def new(self):
    	return super(QuestionManager, self).get_query_set().order_by('-added_at')
    
    
    def popular():
    	return super(QuestionManager, self).get_query_set().order_by('-rating')    
 

class Question(models.Model):
    title = models.CharField(max_length=255) #заголовок вопроса
    text = models.TextField() #полный текст вопроса
    added_at = models.DateTimeField() #дата добавления вопроса
    rating = models.IntegerField() #рейтинг вопроса (число)
    author = models.CharField(max_length=255) #автор вопроса
    likes = models.ManyToManyField(User) #список пользователей, поставивших "лайк"
    objects = QuestionManager()
    
class Answer(models.Model):    
    text = models.TextField() #текст ответа
    added_at = models.DateTimeField(auto_now_add = True) #дата добавления ответа
    question = models.ForeignKey(Question, on_delete = models.PROTECT) #вопрос, к которому относится ответ
    author = models.ForeignKey(User, on_delete = models.PROTECT) #автор ответа    
 
 


