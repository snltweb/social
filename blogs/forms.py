from django import forms
from .models import Post,Comment

# form post blogs
class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':3,
            'placeholder':'Say Something...'
        }))
    class Meta:
        model = Post
        fields =['body']

# form comment blogs
class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))
    class Meta:
        model = Comment
        fields = ['comment']