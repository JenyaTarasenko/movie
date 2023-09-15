from django import forms
from .models import Reviews, RatingStar, Rating


class ReviewForm(forms.ModelForm):
    """форма отзывов"""
    class Meta:
        model = Reviews#поле модели
        fields = ("name", "email", "text")





class RatingForm(forms.Form):
    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)


    class Meta:
        model = Rating
        fields = ('star',)
