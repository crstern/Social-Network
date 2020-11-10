from django import forms

class NewPostForm(forms.Form):
    body = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            'class' : 'form-control col-9 entry_content h-50',
            'rows':'3',
            'placeholder':'What are you thinking about?'
        }))
    