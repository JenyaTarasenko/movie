from django import template
from movies.models import Category, Movie



register = template.Library()#ригестрация тэгов



@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.simple_tag()
def get_last_movies():
    """Последние 5ть """
    movies = Movie.objects.order_by("id")[:5]
    return {"last_movie": movies}

