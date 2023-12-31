from datetime import date

from django.urls import reverse
from django.db import models
from django.shortcuts import render


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категории", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Актеры и режисеры"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})#делает ссылку как на актеров так и на режисеров

    class Meta:
        verbose_name = "Актеры и режисеры"
        verbose_name_plural = "Актеры и режисеры"

class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Жанр", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """фильмы"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2020)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режисер", related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='film_actor')#используя related_name='film_actor' можно сделать узкий запрос к базе
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world_premier = models.DateTimeField("Примьера в мире", auto_now_add=True)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text='указывать сумму в доларах')
    fees_in_usa = models.PositiveIntegerField('Сборы в США', default=0, help_text='Указывать сумму в доларах')
    fess_in_world = models.PositiveIntegerField('Сборы в Мире', default=0, help_text='Указывать сумму в доларах')
    category = models.ForeignKey(Category, verbose_name='Категория',on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)# в url будут прописыватся slug фильма
    draft = models.BooleanField("Черновик", default=False)




    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return render('movie_detail', kwargs={'slug': self.url})


    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"



class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title



    class Meta:
        verbose_name = "Кадры из фильма"
        verbose_name_plural = "Кадры из фильма"



class RatingStar(models.Model):
    """Звезды рейтинга"""
    value = models.PositiveIntegerField("Значение", default=0)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезда рейтинга"
        ordering = ["-value"]




class Rating(models.Model):
    """рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезды")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм")

    def __str__(self):
        return f"{self.star}-{self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"




class Reviews(models.Model):
    """отзывы к фильму"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сщщбщение", max_length=500)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)#self запись ссылается на запись в этой же таблице
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name}-{self.movie}"


    class Meta:
        verbose_name = "Отзывы"
        verbose_name_plural = "Отзывы"












