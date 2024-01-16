from django import forms
from .models import QuizRating


class QuizRatingForm(forms.ModelForm):

    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
    )
    class Meta:
        model = QuizRating
        fields = ['rating']
