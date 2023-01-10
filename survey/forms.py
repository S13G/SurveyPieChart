from django import forms


class SurveyForm(forms.Form):
    question = forms.CharField(label='question')
    OPTIONS = (
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
        ('option5', 'Option 5'),

    )
    answer = forms.ChoiceField(choices=OPTIONS, widget=forms.RadioSelect)
