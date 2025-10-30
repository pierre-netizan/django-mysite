from django import forms
from .models import Comment

class EmailPostForm(forms.Form):#Form只用来校验数据而不会落盘，现在可用Pydantic或Django-ninja来做数据校验
    name=forms.CharField(max_length=25)
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(
        required=False,
        widget=forms.Textarea
    )


class CommentForm(forms.ModelForm):#校验后数据要落盘所以用ModelForm
    class Meta:
        model=Comment
        fields=['name','email','body']
