from django import forms
from django.db.models import fields
from django.forms import widgets
from blog.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
        )
        
        widgets = {
                    'content': forms.Textarea(attrs={
                                        'class': 'input-text',
                                        'placeholder': 'Comment here'
                                    })
                }
        