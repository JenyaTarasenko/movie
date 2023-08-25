from django import forms
from .models import Reviews



class ReviewForm(forms.ModelForm):
    """форма отзывов"""
    class Meta:
        model = Reviews#поле модели
        fields = ("name", "email", "text")



