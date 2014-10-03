from django import forms


class EditArticleForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        error_messages={'required': 'You should enter a title.'}
    )
    source_url = forms.URLField(required=False)
    content = forms.CharField(
        error_messages={'required': 'You should enter the content.'}
    )
