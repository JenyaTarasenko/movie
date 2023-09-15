from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView

from .models import *
from .forms import ReviewForm, RatingForm


class GenreYear:
    """
    Жанры и года вывода фильмов
    """

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter().values("year")#.values_list("year")#.values_list("year")  # те фильмы которые не черновики


# class MovieWievs(View):
#     """Список фильмов"""
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, 'movie/index.html', {'movie_list': movies})

class MovieWievs(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)#фильтрует поле по умолчанию (не черновик)
    template_name = 'movie/movie_list.html'
    #paginate_by = 1 #пагинация



    # def get_context_data(self, *args, **kwargs):
    #     """
    #     Метод категории
    #     """
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

      # прописываем этот метод в templattetags




# class MovieDetail(View):
#     """Детальная информация фильма"""
#     def get(self, request, slug):
#         movies = Movie.objects.get(url=slug)#get метод который получает одну запись pk это id
#         return render(request, 'movie/movie_detail.html', {'movies_list': movies})


class MovieDetail(GenreYear, DetailView):
    """Детальная информация фильма"""
    model = Movie
    slug_field = 'url'#по какому полю нужно искать запесь
    template_name = 'movie/movie_detail.html'


    def get_context_data(self, **kwargs):#метод рейтинга
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context



class AddReview(View):
    """отзывы"""
    # def post(self, request, pk):
    #   print(request.POST)
    #   return redirect("/")
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        return redirect("/")


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movie/actor.html'
    slug_field = "name"#по полю name Actor



class FilterMoviesView(GenreYear,ListView):
    """
    Фильтр фильмов
    """
    def get_queryset(self):
        """
        поиск по жанрам и и годам на панели сайтбар
        """
        queryset = Movie.objects.filter(
            year__in=self.request.GET.getlist('year'), genres__in=self.request.GET.getlist("genre")
        )
        return queryset

class AddStarRating(View):
    """
    Добавить рейтинг к фильму
    """
    def get_client_ip(self, request):
        x_forvarded_for = request.META.get("HTTP_X_FOEWARDED_FOR")
        if x_forvarded_for:
            ip =x_forvarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)



class Search(ListView):
    """поиск фильмов"""
    # paginate_by = 2
    def queryset(self):
        return Movie.objects.filter(title__incontains=self.request.GET.get('q'))

    # def get_context_data(self, *args, **kwargs):
    #         context = super().get_context_data(*args, **kwargs)
    #         context["q"] = f'q={self.request.GET.get("q")}&'
    #         return context