from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User


class AskForm(forms.Form):
    title = forms.CharField(label='Заголовок вопроса', max_length=1000)
    text = forms.CharField(label='Текст вопроса', max_length=1000)
    	
    
class AnswerForm(forms.Form):
    text = forms.CharField(label='Текст ответа', max_length=1000)
    question = forms.ModelChoiceField(label='Выберите вопрос', queryset=Question.objects.values_list('id',flat=True), widget=forms.Select())
    
        
class SignupForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=1000)
    email = forms.EmailField(label='email', max_length=1000)
    password = forms.CharField(label='Пароль', max_length=1000)
    
    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user
        

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=1000)
    password = forms.CharField(label='Пароль', max_length=1000)

    
    
  
