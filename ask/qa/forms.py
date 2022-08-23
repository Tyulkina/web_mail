from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User

class AskForm(forms.Form):
    title = forms.CharField(label='Заголовок вопроса', max_length=1000)
    text = forms.CharField(label='Текст вопроса', max_length=1000)
    	
    def save(self):
    	question = Question(**self.cleaned_data)
    	user = User.objects.get(id=1)
    	question.author=user
    	question.save()
    	return question	
    
    
class AnswerForm(forms.Form):
    text = forms.CharField(label='Текст ответа', max_length=1000)
    #question_list=Question.objects.values_list('id','title')
    #question = forms.CharField(label='Выберите вопрос',widget=forms.Select(choices=question_list))
    question = forms.ModelChoiceField(label='Выберите вопрос', queryset=Question.objects.values_list('id',flat=True), widget=forms.Select())
    
    def save(self): # custom validation
        answer = Answer(**self.cleaned_data)
        user = User.objects.get(id=1)
        answer.author=user        
        answer.save()
        return answer	
        

