from django import forms
from .models import Comment



#Форма комментариев 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)
        widgets = {
          'comment_text': forms.Textarea(attrs=
          	{'name':'text','class':'form-control w-100',
          	'placeholder':'Комментарий', 'rows': 4, 'cols': 40,}),
        }


    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment_text'].label = ""




