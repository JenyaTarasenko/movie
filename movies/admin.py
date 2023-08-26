from django.contrib import admin
from .models import *


@admin.register(Category)#регистрация через декоратор
class CategoryAdmin(admin.ModelAdmin):
    """
     категории
    """
    list_display = ('id', 'name', 'description', 'url')
    list_display_links = ('name',)#имя поля которое будет ссылкой



class ReviewInline(admin.StackedInline):
    """
    Передать все отзывы к фильму класс должен
    быть написан выше данный атрибут работает many-to-many, faregn-key
    """
    model = Reviews
    extra = 1#доп поле



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Фильмы поиск
    """
    list_display = ('title', 'category', 'description', 'url', 'draft')
    list_filter = ('category', 'year', 'actors',)#фильтрация фильмов по категориям
    search_fields = ('title', 'category__name')#фильтрация поля по title,category
    inlines = [ReviewInline]#класс подвязан к фильму







@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """
    Отзывы
    """
    list_display = ('name', 'email', 'movie', 'parent', 'id')
    readonly_fields = ('name', 'email')#поля скрыты от редактирования





#admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
#admin.site.register(Movie)
admin.site.register(MovieShots)
admin.site.register(Actor)
admin.site.register(Rating)
admin.site.register(RatingStar)
#admin.site.register(Reviews)


