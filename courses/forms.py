from django import forms


class OpenCourseForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        error_messages={'required': 'You must give your course a name.'}
    )
    short_description = forms.CharField(max_length=200, required=False)
